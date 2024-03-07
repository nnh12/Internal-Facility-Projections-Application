from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.access_list import user_orgs

from data_upload_system.models import Organization
from django.db import models


class MyOrganizations(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    organizations = models.ManyToManyField(to=Organization)

    @receiver(post_save, sender=User)  # add this
    def createMyOrganizations(sender, instance: User, created, **kwargs):
        if created:
            MyOrganizations.objects.create(user=instance)
            if instance.username in user_orgs:
                for orgId in user_orgs[instance.username]:
                    instance.myorganizations.organizations.add(Organization.objects.get(id=str(orgId)))
            instance.myorganizations.save()


class AuthorizedNetID(models.Model):
    netID = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.netID

@receiver(post_save, sender=AuthorizedNetID)
def createUserIfNecessary(sender, instance: AuthorizedNetID, created, **kwargs):
    if created:
        User.objects.get_or_create(username=instance.netID)
