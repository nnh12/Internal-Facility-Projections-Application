import logging

from django_cas_ng.backends import CASBackend
from django.contrib.auth.models import User
from accounts.access_list import user_orgs
from accounts.models import AuthorizedNetID


logger = logging.getLogger('django')

class AuthGuardCASBackend(CASBackend):
    authorizedUsers = list(user_orgs.keys())

    def user_can_authenticate(self, user):
        return True

    def bad_attributes_reject(self, request, username, attributes):
        #Will prevent anyone with the username that is not in the predefined authorizedUsers list and not in the
        #AuthorizedNetID table.
        if username not in self.authorizedUsers and not AuthorizedNetID.objects.filter(netID=username).exists() and not User.objects.filter(username=username).exists():
            logger.error("UnsuccessfulLoginError: {0} attempted to log in but was not registered".format(username))
            return True

        return False
