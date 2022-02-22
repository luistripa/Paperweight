from django.urls import path

import documents.views as documents

app_name = 'documents'
urlpatterns = [
    path('dossiers/', documents.DossiersListView.as_view(), name='dossier_list'),
    path('dossiers/new', documents.DossierCreateView.as_view(), name='dossier_create'),
    path('dossiers/<int:pk>/edit', documents.DossierUpdateView.as_view(), name='dossier_update'),
    #path('dossiers/<str:search_string>', documents.dossiers_view),
    path('dossiers/<int:dossier_id>/sections/', documents.SectionsListView.as_view(), name='section_list'),
    path('dossiers/<int:dossier_id>/sections/new', documents.SectionsCreateView.as_view(), name='section_create'),
    path(
        'dossiers/<int:dossier_id>/sections/<int:pk>/edit',
        documents.SectionsUpdateView.as_view(),
        name='section_update'
    ),
    path(
        'dossiers/<int:dossier_id>/sections/<int:section_id>',
        documents.DocumentListView.as_view(),
        name='document_list'
    ),
    path(
        'dossiers/<int:dossier_id>/sections/<int:section_id>/documents/<int:pk>',
        documents.DocumentDetailView.as_view(),
        name='document_detail'
    ),
    path(
        'dossiers/<int:dossier_id>/sections/<int:section_id>/documents/new',
        documents.DocumentCreateView.as_view(),
        name='document_create'
    ),
    path(
        'dossiers/<int:dossier_id>/sections/<int:section_id>/documents/<int:pk>/edit',
        documents.DocumentUpdateView.as_view(),
        name='document_update'
    ),
    path(
        'dossiers/<int:dossier_id>/sections/<int:section_id>/documents/<int:document_id>/download',
        documents.DocumentDownloadView.as_view(),
        name='document_download',
    ),

    path('dossiers/search/', documents.DocumentSearchView.as_view(), name='search'),
    path('dossiers/<int:dossier_id>/sections_json', documents.sections_from_dossier_as_json),
    path('tags/', documents.documents_tags_list_as_json),
]
