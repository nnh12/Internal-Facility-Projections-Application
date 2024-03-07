from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from data_upload_system.models import Record, UploadHistory, RecordArchive, UploadHistoryArchive, ArchiveHistory
from projections_update_system.models import ProjectionsUpdateLog, ProjectionsUpdateLogArchive


@login_required
@staff_member_required
def archiveIndex(request):
    return render(request, "archive/archive.html", {
        "numRecords": Record.objects.count(),
        "histories": ArchiveHistory.objects.all().order_by("-timestamp").values()
    })


@login_required
@staff_member_required
def commitArchive(request):
    fiscalYear = Record.objects.first().fiscal_year
    numRows = 0
    username = "admin"
    if request.user is not None:
        user = request.user
        username = user.first_name + " " + user.last_name + ' (' + user.username + ')'

    # Need to archive records, upload history and change logs
    for record in Record.objects.all():
        recordArchive = RecordArchive()
        for field in record._meta.fields:
            setattr(recordArchive, field.name, getattr(record, field.name))
        recordArchive.pk = None
        recordArchive.save()
        numRows += 1

    for uploadHistory in UploadHistory.objects.all():
        uploadHistoryArchive = UploadHistoryArchive()
        for field in uploadHistory._meta.fields:
            setattr(uploadHistoryArchive, field.name, getattr(uploadHistory, field.name))
        uploadHistoryArchive.pk = None
        uploadHistoryArchive.save()

    for projectionsUpdateLog in ProjectionsUpdateLog.objects.all():
        projectionsUpdateLogArchive = ProjectionsUpdateLogArchive()
        for field in projectionsUpdateLog._meta.fields:
            setattr(projectionsUpdateLogArchive, field.name, getattr(projectionsUpdateLog, field.name))
        projectionsUpdateLogArchive.pk = None
        projectionsUpdateLogArchive.save()

    Record.objects.all().delete()
    UploadHistory.objects.all().delete()
    ProjectionsUpdateLog.objects.all().delete()

    ArchiveHistory(fiscalYear=fiscalYear, rows=numRows, byUsername=username).save()

    return HttpResponseRedirect("/data/archive/")