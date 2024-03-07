"""
This is a file that must be run the first time that the server is run or the database is completely wiped.
This will setup the bare minimum initializations necessary for the server to run.
However,
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projections.settings")
import django
django.setup()

from accounts.access_list import user_orgs
from accounts.models import AuthorizedNetID

def loadFixtures():
    print("Loading fixture data")
    stream1 = os.popen("python manage.py loaddata data_upload_system/fixtures/organization_data.json data_upload_system/fixtures/organization_data.json")
    print(stream1)
    stream2 = os.popen("python manage.py loaddata data_upload_system/fixtures/organization_data.json data_upload_system/fixtures/accountParentLevelE_data.json")
    print(stream2)


def setupAuthorizedAccounts():
    """
    Will setup the authorized accounts on the server
    :return:
    """
    print("Setting up authorized accounts")
    for key in user_orgs.keys():
        AuthorizedNetID.objects.get_or_create(netID=key)
    print("Authorized accounts setup complete")





if __name__ == '__main__':
    setupAuthorizedAccounts()
    print("Setup complete")