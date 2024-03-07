import datetime

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginSessionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.

        Will log out the user daily to force reauthentication
        """
        # LAST_ACTIVE_TIME = 'last_active_time'
        # print(request.user)
        # print(datetime.datetime.now().strftime("%m/%d/%Y"))
        # print(request.user.is_authenticated)
        # if not request.user.is_authenticated:
        #     # Can't log out if not logged in
        #     return None
        #
        # # auth.logout(request)
        #
        # #Get the current date
        # current_datetime = datetime.datetime.now().strftime("%m/%d/%Y %M")
        #
        # if LAST_ACTIVE_TIME in request.session:
        #     #Compare the current datetime and the last active variable in session
        #     last_active = datetime.datetime.strptime(request.session[LAST_ACTIVE_TIME], "%m/%d/%Y %M")
        #     current_datetime_as_obj = datetime.datetime.strptime(current_datetime, "%m/%d/%Y %M")
        #
        #     #If there is a previous date then automatically log out
        #     if last_active < current_datetime_as_obj:
        #         del request.session[LAST_ACTIVE_TIME]
        #         auth.logout(request)
        #         return HttpResponseRedirect(reverse("cas_ng_login"))
        #
        # #Update the last logged in time in the session
        # request.session[LAST_ACTIVE_TIME] = current_datetime

        return None
