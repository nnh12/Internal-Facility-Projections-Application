from django.urls import path
from .views.delete import delete
from .views.upload import upload
from .views.index import index
from .views.archive import archiveIndex, commitArchive

urlpatterns = [
    path('', index, name='dataIndex'),
    path('upload/', upload, name='upload'),
    path('delete/', delete, name='delete'),
    path('archive/', archiveIndex, name='archiveIndex'),
    path('archive/commit', commitArchive, name='commitArchive')
]
