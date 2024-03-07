from django.urls import path
from .views import projectionsHomepage, updateProjections, selectOrgToUpdate, getDetailRecord, viewRecordInformation, viewLogs

urlpatterns = [
    path('', projectionsHomepage, name='projectionsHomepage'),
    path('detailRecord', getDetailRecord, name='detailRecord'),
    path('viewRecordInformation', viewRecordInformation, name='viewRecordInformation'),
    path('organizations', selectOrgToUpdate, name='selectOrgToUpdate'),
    path('update/<int:org_id>', updateProjections, name='updateProjections'),
    path('logs/', viewLogs, name='logs'),
]
