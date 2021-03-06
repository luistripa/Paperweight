import mimetypes

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, FileResponse, JsonResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from Paperweight.settings import MEDIA_ROOT
from documents.forms import *

import os
import random
import string

# Create your views here.


def index(request: HttpRequest, *args, **kwargs):
    return render(request, 'index.html', context={})


def sections_from_dossier_as_json(request: HttpRequest, *args, **kwargs):
    dossier = Dossiers.objects.get(id=kwargs.get('dossier_id', None))
    sections_serialized = serializers.serialize('json', dossier.sections_set.all(), fields='name')
    return JsonResponse({'sections': sections_serialized})


def documents_tags_list_as_json(request: HttpRequest, *args, **kwargs):
    search_text = request.GET.get('text', None)

    if search_text == "":
        return JsonResponse({'tags': '[]'})

    tags = Tags.objects.filter(name__contains=search_text)

    tags_serialized = serializers.serialize('json', tags, fields='name')

    return JsonResponse({'tags': tags_serialized})


class DossiersListView(LoginRequiredMixin, ListView):
    model = Dossiers
    template_name = 'documents/dossiers/dossier_list.html'


class DossierCreateView(LoginRequiredMixin, CreateView):
    model = Dossiers
    template_name = 'documents/dossiers/dossier_create.html'
    fields = ['name']
    success_url = reverse_lazy('documents:dossier_list')

    def form_valid(self, form):
        object = form.save()
        object.owner = self.request.user.profile
        object.save()
        return super(DossierCreateView, self).form_valid(form)


class DossierUpdateView(LoginRequiredMixin, UpdateView):
    model = Dossiers
    template_name = 'documents/dossiers/dossier_update.html'
    fields = ['name']
    success_url = reverse_lazy('documents:dossier_list')


class DossierDeleteView(LoginRequiredMixin, DeleteView):
    model = Dossiers
    template_name = 'documents/dossiers/dossier_delete.html'

    def get_success_url(self):
        return reverse('documents:dossier_list')


class SectionsListView(LoginRequiredMixin, ListView):
    model = Sections
    template_name = 'documents/sections/section_list.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SectionsListView, self).get_context_data(object_list=object_list, **kwargs)
        context['dossier'] = Dossiers.objects.get(id=self.kwargs.get('dossier_id'))
        return context

    def get_queryset(self):
        dossier_id = self.kwargs.get('dossier_id', None)

        try:
            dossier = Dossiers.objects.get(id=dossier_id)
            return dossier.sections_set.get_queryset()

        except Dossiers.DoesNotExist:
            return Sections.objects.none()
        

class DossierMixin:
    dossier = None
    
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        dossier_id = kwargs.get('dossier_id')
        self.dossier = Dossiers.objects.get(id=dossier_id)
        return super(DossierMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(DossierMixin, self).get_context_data(*args, **kwargs)
        context['dossier'] = Dossiers.objects.get(id=self.kwargs.get('dossier_id'))
        return context


class SectionMixin(DossierMixin):
    section = None

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        section_id = kwargs.get('section_id')
        self.section = Sections.objects.get(id=section_id)
        return super(SectionMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SectionMixin, self).get_context_data(*args, **kwargs)
        context['section'] = Sections.objects.get(id=self.kwargs.get('section_id'))
        return context


class SectionsCreateView(LoginRequiredMixin, DossierMixin, CreateView):
    model = Sections
    template_name = 'documents/sections/section_create.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.dossier = self.dossier
        form.instance.owner = self.request.user.profile
        object = form.save()
        return redirect('documents:document_list', self.dossier.id, object.id)


class SectionsUpdateView(LoginRequiredMixin, DossierMixin, UpdateView):
    model = Sections
    template_name = 'documents/sections/section_update.html'
    fields = ['name']

    def form_valid(self, form):
        form.save()
        return redirect('documents:section_list', self.dossier.id)


class SectionsDeleteView(LoginRequiredMixin, DossierMixin, DeleteView):
    model = Sections
    template_name = 'documents/sections/section_delete.html'

    def get_success_url(self):
        return reverse(
            'documents:section_list',
            kwargs={
                'dossier_id': self.dossier.id,
            })


class DocumentListView(LoginRequiredMixin, SectionMixin, ListView):
    model = Document
    template_name = 'documents/documents/document_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocumentListView, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def get_queryset(self):
        dossier_id = self.kwargs.get('dossier_id', None)
        section_id = self.kwargs.get('section_id', None)

        try:
            dossier = Dossiers.objects.get(id=dossier_id)
            section = Sections.objects.get(id=section_id, dossier=dossier)
            return section.document_set.get_queryset()

        except Dossiers.DoesNotExist or Sections.DoesNotExist:
            return QuerySet()


class DocumentCreateView(LoginRequiredMixin, SectionMixin, CreateView):
    model = Document
    template_name = 'documents/documents/document_create.html'
    form_class = NewDocumentForm

    def form_valid(self, form):
        tag_list_as_str = form.cleaned_data['tags']
        tag_list = tag_list_as_str.strip().split(' ')

        form.instance.owner = self.request.user.profile
        form.instance.section = Sections.objects.get(id=self.kwargs.get('section_id', None))

        # Get file
        file: InMemoryUploadedFile = self.request.FILES.get('file', None)
        file_data = file.read()
        file_name = create_file(file, file_data)

        form.instance.file_path = file_name

        form.save()

        for tag_str in tag_list:
            if tag_str == "":
                continue
            tag, created = Tags.objects.get_or_create(name=tag_str)
            form.instance.tags.add(tag)

        return redirect('documents:document_list', self.kwargs.get('dossier_id'), self.kwargs.get('section_id', None))


class DocumentUpdateView(LoginRequiredMixin, SectionMixin, UpdateView):
    model = Document
    template_name = 'documents/documents/document_update.html'
    form_class = EditDocumentForm

    def form_valid(self, form):
        document: Document = form.instance

        tag_list_as_str = form.cleaned_data['tags']
        tag_list = tag_list_as_str.strip().split(' ')

        # Get file
        file: InMemoryUploadedFile = self.request.FILES.get('file', None)

        if file is not None:
            if os.path.exists(document.file_path.path):
                os.remove(document.file_path.path)
            file_data = file.read()
            file_name = create_file(file, file_data)

            form.instance.file_path = file_name

        document.tags.set(Tags.objects.none())
        for tag_str in tag_list:
            if len(tag_str) == 0:
                continue
            tag, created = Tags.objects.get_or_create(name=tag_str)
            document.tags.add(tag)

        document.save()

        # Delete tags with no documents associated
        tags_to_delete = Tags.objects.filter(document__isnull=True)
        tags_to_delete.delete()

        return redirect('documents:document_list', self.kwargs.get('dossier_id'), self.kwargs.get('section_id', None))


class DocumentDetailView(LoginRequiredMixin, SectionMixin, DetailView):
    model = Document
    template_name = 'documents/documents/document_detail.html'


class DocumentDownloadView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, *args, **kwargs):
        dossier_id = kwargs.get('dossier_id', None)
        section_id = kwargs.get('section_id', None)
        document_id = kwargs.get('document_id', None)
        try:
            document = Document.objects.get(id=document_id, protection_level__lte=request.user.profile.permissions)
        except Document.DoesNotExist:
            messages.error(request=request, message='Document could not be found')
            return HttpResponseRedirect(f'/documents/{dossier_id}/{section_id}')
        else:
            return FileResponse(
                open(document.file_path.path, 'rb'),
                content_type=mimetypes.guess_type(document.file_path.path),
                as_attachment=False,
                filename=f'{document.name}{document.extension()}'
            )


class DocumentDeleteView(LoginRequiredMixin, SectionMixin, DeleteView):
    model = Document
    template_name = 'documents/documents/document_delete.html'

    def get_success_url(self):
        return reverse(
            'documents:document_list',
            kwargs={
                'dossier_id': self.dossier.id,
                'section_id': self.section.id
            })


class DocumentSearchView(LoginRequiredMixin, FormView):
    form_class = DocumentSearchForm
    template_name = 'documents/search.html'

    def form_valid(self, form):
        documents = Document.objects.all()
        if form.cleaned_data['dossier'] is not None:
            documents = documents.filter(section__dossier=form.cleaned_data['dossier'])

        if form.cleaned_data['section'] is not None:
            documents = documents.filter(section=form.cleaned_data['section'])

        if form.cleaned_data['name'] != '':
            documents = documents.filter(name__contains=form.cleaned_data['name'])

        tag_str_list = form.cleaned_data['tags'].strip().split(" ")
        if tag_str_list != '':
            tags = Tags.objects.filter(name__in=tag_str_list)
            for tag in tags:
                documents = documents.filter(tags=tag)

        return render(self.request, 'documents/search_results.html', context={'object_list': documents})


def create_file(file: InMemoryUploadedFile, data: bytes):
    while True:
        _, extension = os.path.splitext(file.name)
        file_path = generate_filename(extension)
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(data)
            return file_path


def generate_filename(extension: str):
    file_name = ""
    for i in range(0, 10):
        letter = random.choice(string.ascii_lowercase)
        file_name += letter
    return os.path.join(MEDIA_ROOT, file_name + extension)
