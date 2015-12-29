from club.models import Member, Activity
from django.contrib import admin
from reversion.admin import VersionAdmin

class MemberModelAdmin(VersionAdmin):
    list_display = ('name', 'sex', 'balance', 'weight')
    ordering = ('-weight', )

class ActivityModelAdmin(VersionAdmin):
    pass

admin.site.register(Member, MemberModelAdmin)
admin.site.register(Activity, ActivityModelAdmin)
