from django import forms

from documents.models import *


class NewDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name']
    tags = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'hidden': True}), required=False)
    file = forms.FileField(required=True)


class DocumentSearchForm(forms.Form):
    dossier = forms.ModelChoiceField(
        Dossiers.objects.all(),
        empty_label='All',
        required=False,
        widget=forms.Select(attrs={'onchange': 'updateSections(this)'})
    )
    section = forms.ModelChoiceField(Sections.objects.all(), empty_label='All', required=False)
    name = forms.CharField(label='Document Name: ', required=False)
    tags = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'hidden': True}), required=False)
