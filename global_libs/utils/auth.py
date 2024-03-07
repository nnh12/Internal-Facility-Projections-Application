from accounts.models import AuthorizedNetID
from django.contrib.auth.models import User


def createNewAuthorizedUser(netID, isStaff, isSuperUser):
    """
    Creates a new authorized user
    :param netID: NetID of the new authorized user
    :param isStaff: Is the user to be a staff member
    :return:
    """
    if isStaff != False and isStaff != True:
        print("Expected isStaff to be a boolean. No user has been created")
        return

    if isSuperUser != False and isSuperUser != True:
        print("Expected isSuperUser to be a boolean. No user has been created")
        return

    netID = str(netID)
    newUser, _ = AuthorizedNetID.objects.get_or_create(netID=netID)
    newUser.save()
    if not User.objects.filter(username=netID).exists():
        print("Error in creating user.")
        try:
            AuthorizedNetID.objects.filter(netID=netID).delete()
        except:
            pass
    else:
        user = User.objects.get(username=netID)
        user.is_staff = isStaff
        user.is_superuser = isSuperUser
        user.save()
        print("Created new user :{0}".format(newUser.netID))
