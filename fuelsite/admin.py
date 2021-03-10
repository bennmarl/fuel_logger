
### Register your models here.

### Ensures default Organization model interfaces are hidden
### Substitute form class on AccountUser admin

from django.contrib import admin
from organizations.models import (Organization, OrganizationUser,
    OrganizationOwner)
from .forms import AccountUserForm
from .models import Organization, AccountUser

class AccountUserAdmin(admin.ModelAdmin):
    form = AccountUserForm

#admin.site.unregister(Organization)
#admin.site.unregister(OrganizationUser)
#admin.site.unregister(OrganizationOwner)
admin.site.register(Organization)
admin.site.register(AccountUser, AccountUserAdmin)