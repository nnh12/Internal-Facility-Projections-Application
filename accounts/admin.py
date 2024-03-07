from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import MyOrganizations, AuthorizedNetID


class MyOrganizationInline(admin.StackedInline):
    model = MyOrganizations
    can_delete = False
    verbose_name_plural = 'My Organization'
    fk_name = 'user'
    filter_horizontal = ('organizations',)

class CustomUserAdmin(UserAdmin):
    inlines = (MyOrganizationInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# class MyOrganizationAdmin(admin.ModelAdmin):


admin.site.register(MyOrganizations)
admin.site.register(AuthorizedNetID)
