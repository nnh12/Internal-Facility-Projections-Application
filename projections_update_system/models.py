from django.db import models


class BaseProjectionsUpdateLog(models.Model):
    class Meta:
        abstract = True

    accE = models.ForeignKey('data_upload_system.AccountParentLevelE', on_delete=models.CASCADE)
    org = models.ForeignKey('data_upload_system.Organization', on_delete=models.CASCADE)
    byUserName = models.CharField(max_length=50)
    fromValue = models.FloatField()
    toValue = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "[{0}, {1}] Update for {2} in {3}".format(self.timestamp, self.byUserName, self.accE.name, self.org)


class ProjectionsUpdateLog(BaseProjectionsUpdateLog):
    pass


class ProjectionsUpdateLogArchive(BaseProjectionsUpdateLog):
    pass


class CurrentProjections(models.Model):
    account = models.CharField(max_length=50, null=True, blank=True)
    program = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    activity = models.CharField(max_length=100, null=True, blank=True)
    accE = models.ForeignKey('data_upload_system.AccountParentLevelE', on_delete=models.CASCADE)
    org = models.ForeignKey('data_upload_system.Organization', on_delete=models.CASCADE)
    projection = models.FloatField(default=0)
    comments = models.CharField(max_length=1500, null=True, blank=True)
    lastUpdatedFiscalMonth = models.IntegerField(null=True, blank=True)
    lastUpdatedYear = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return "Projection for " + self.accE.name + " in Org " + self.org.name + "is " + str(self.projection)