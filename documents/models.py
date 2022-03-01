import os

from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.http import HttpRequest
from django.utils import timezone

# Create your models here.
from Paperweight import settings
from registration.models import ProtectionLevels


class Tags(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class DossiersAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest):
        qs = super(DossiersAdmin, self).get_queryset(request)
        return qs.filter(protection_level__lte=request.user.profile.permissions)


class Dossiers(models.Model):
    class Meta:
        verbose_name = 'Dossier'
        verbose_name_plural = 'Dossiers'

    owner = models.ForeignKey('registration.Profile', on_delete=models.SET_NULL, null=True,  blank=True)
    protection_level = models.IntegerField(choices=ProtectionLevels.CHOICES, default=ProtectionLevels.PUBLIC)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class SectionsAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest):
        qs: QuerySet[Sections] = super(SectionsAdmin, self).get_queryset(request)
        return qs.filter(protection_level__lte=request.user.profile.permissions)


class Sections(models.Model):
    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    owner = models.ForeignKey('registration.Profile', on_delete=models.SET_NULL, null=True,  blank=True)
    protection_level = models.IntegerField(choices=ProtectionLevels.CHOICES, default=ProtectionLevels.PUBLIC)
    dossier = models.ForeignKey('Dossiers', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.dossier.name} - {self.name}"

    def __repr__(self):
        return self.name


class AuditLog(models.Model):
    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'

    CREATE = 1
    DOWNLOAD = 2
    VIEW = 3
    ACTIONS = (
        (CREATE, 'Create'),
        (DOWNLOAD, 'Download'),
        (VIEW, 'View')
    )
    type = models.IntegerField(choices=ACTIONS)
    profile = models.ForeignKey('registration.Profile', on_delete=models.CASCADE)
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.ACTIONS[self.type-1][1]} - {self.profile.user.username}'

    def __repr__(self):
        return f'<AuditLog ({self.ACTIONS[self.type-1][1]} - {self.profile.user.username})>'


class DocumentAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest):
        qs: QuerySet = super(DocumentAdmin, self).get_queryset(request)
        return qs.filter(protection_level__lte=request.user.profile.permissions)


class Document(models.Model):
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    owner = models.ForeignKey('registration.Profile', on_delete=models.SET_NULL, null=True,  blank=True)
    protection_level = models.IntegerField(choices=ProtectionLevels.CHOICES, default=ProtectionLevels.PUBLIC)
    section = models.ForeignKey('Sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    file_path = models.FileField()

    tags = models.ManyToManyField('Tags', blank=True)

    def extension(self):
        name, extension = os.path.splitext(self.file_path.name)
        return extension

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


@receiver(pre_delete, sender=Document)
def remove_file_before_delete(sender, instance: Document, **kwargs):
    try:
        os.remove(instance.file_path.path)
    except ValueError:
        pass
