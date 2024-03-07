import uuid
from django.contrib import admin

from django.contrib.auth.models import Group
from django.db import models

from projections_update_system.models import CurrentProjections


class BaseRecord(models.Model):
    class Meta:
        abstract = True

    fiscal_year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    upload_id = models.UUIDField()

    fund_type_parent_level_A = models.CharField(max_length=50)
    fund_type_parent_level_B = models.CharField(max_length=50)
    fund_type = models.CharField(max_length=50)

    fund_source_parent_level_C = models.CharField(max_length=50)
    fund_source_parent_level_D = models.CharField(max_length=50)
    fund_source = models.CharField(max_length=50)

    organization_parent_level_B = models.CharField(max_length=50)
    organization_parent_level_C = models.CharField(max_length=50)
    organization_parent_level_D = models.CharField(max_length=50)
    organization_parent_level_E = models.CharField(max_length=50)
    organization = models.CharField(max_length=50)

    account_parent_level_B = models.CharField(max_length=50)
    account_parent_level_C = models.CharField(max_length=50)
    account_parent_level_D = models.CharField(max_length=50)
    account_parent_level_E = models.CharField(max_length=50)
    account = models.CharField(max_length=50)

    budget_amount = models.FloatField()
    actual_YTD_beginning_of_period = models.FloatField()
    period_net = models.FloatField()
    actual_YTD_end_of_period = models.FloatField()
    PO_Req_other_encumbrances = models.FloatField()
    salary_encumbrance = models.FloatField()
    remaining_budget = models.FloatField()

    program = models.CharField(max_length=20)
    activity = models.CharField(max_length=20)
    location = models.CharField(max_length=20)

    def __str__(self):
        return "Record for org {0} of account {1} in month {2}, {3}".format(self.organization,
                                                                            self.account_parent_level_E, self.month,
                                                                            self.fiscal_year)

    @property
    def spent_rate(self):
        return ((self.actual_YTD_end_of_period / self.month) * 12) \
               + (self.PO_Req_other_encumbrances + self.salary_encumbrance)

    @property
    def ytd_spent(self):
        return self.actual_YTD_end_of_period + self.PO_Req_other_encumbrances + self.salary_encumbrance


# lynn ytd spent

class Record(BaseRecord):
    pass


class RecordArchive(BaseRecord):
    pass


class Organization(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AccountParentLevelE(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    allowChildProjections = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Account Parent Level E Master'
        verbose_name_plural = 'Account Parent Level E Master Lists'
    # Lynn


class AccountParentLevelEAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)

    # Lynn

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.allowChildProjections:
            CurrentProjections.objects.filter(accE=self).delete()
        super(AccountParentLevelE, self).save(*args, **kwargs)


class BaseUploadHistory(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    byUsername = models.CharField(max_length=50)
    month = models.PositiveSmallIntegerField()
    uploadTime = models.DateTimeField(auto_now_add=True)
    rows = models.PositiveSmallIntegerField()

    def __str__(self):
        return "Upload of {0} by {1} at {2}".format(self.month, self.byUsername, self.uploadTime)


class UploadHistory(BaseUploadHistory):
    pass


class UploadHistoryArchive(BaseUploadHistory):
    pass


class ArchiveHistory(models.Model):
    fiscalYear = models.PositiveSmallIntegerField()
    byUsername = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    rows = models.PositiveSmallIntegerField()

    def __str__(self):
        return "Archive of data from {0} by {1} at {2} with {3} rows".format(self.fiscalYear, self.byUsername,
                                                                             self.timestamp, self.rows)
