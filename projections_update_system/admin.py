from django.contrib import admin

# Register your models here.
from projections_update_system.models import ProjectionsUpdateLog, CurrentProjections
from data_upload_system.models import AccountParentLevelE, AccountParentLevelEAdmin


admin.site.register(ProjectionsUpdateLog)
# admin.site.register(AccountParentLevelE)
admin.site.register(AccountParentLevelE, AccountParentLevelEAdmin)
admin.site.register(CurrentProjections)

