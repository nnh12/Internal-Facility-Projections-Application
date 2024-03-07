import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from data_upload_system.models import UploadHistory
from projections.constants import months
from datetime import datetime

from data_upload_system.util.scriptEmail import sendNotification


def currentMonth():
    return (datetime.now().month - 6) % 12


@login_required
@staff_member_required
def index(request):
    uploadHistories = UploadHistory.objects.all().order_by('-uploadTime').values()
    for row in uploadHistories:
        row['month'] = months[row['month']]

    uploadedMonths = [h['month'] for h in uploadHistories]

    uploadResult = None
    if "uploadResult" in request.session:
        uploadResult = request.session["uploadResult"]
        del request.session["uploadResult"]

    return render(request, "data/uploader.html", {
        # 'months': months[1:currentMonth()],Lynn
        'months': months,
        'history': uploadHistories,
        'uploadedMonths': uploadedMonths,
        "uploadResult": uploadResult
    })


# Helper Functions
def sendNotificationsToOrganizations(user):
    """
    Sends an email notification to all the members of any organization, letting them know the date that they need to submit their
    changes by.
    :param user: User that is sending the broadcast message
    :return:
    """
    signature = "The Rice University Projections Management Tool"
    message = "Good day,\n This is the Rice Projections Application notifying you that {0} {1} ({2}) " \
              "has opened this month's projections to be editted.\n You have until {3} to upload your org's projected " \
              "budget. \n\n\n Thank you.\n\n\n{4}".format(user.first_name, user.last_name, user.email,
                                                 (datetime.datetime.today() + datetime.timedelta(days=7)).strftime(
                                                     "%m/%d/%y"), signature)
    sendNotification(["bss13@rice.edu"], "Projections For {0} {1} Now Open".format(datetime.datetime.today().strftime("%B"), datetime.datetime.today().year), message)


