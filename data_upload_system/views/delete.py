from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from data_upload_system.models import Record, UploadHistory

UPLOAD_ID_KEY = r'upload_id'


@login_required
def delete(request):
    if UPLOAD_ID_KEY in request.POST:
        deleteUpload(request.POST[UPLOAD_ID_KEY])
    return HttpResponseRedirect("/data/")


def deleteUpload(upload_id):
    Record.objects.filter(upload_id__exact=upload_id).delete()
    UploadHistory.objects.filter(id=upload_id).delete()
