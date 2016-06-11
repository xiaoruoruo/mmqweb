from club.models import Member, Activity
from django.contrib import admin
from reversion.admin import VersionAdmin
from reversion import revisions as reversion

class MemberModelAdmin(VersionAdmin):
    list_display = ('name', 'sex', 'balance', 'weight')
    ordering = ('-weight', )

def activity_change_date(modeladmin, request, queryset):
    with reversion.create_revision():
        queryset.update(date='2016-01-17')
        reversion.set_user(request.user)
        reversion.set_comment('Activity bulk change date')
activity_change_date.short_description = "Change activity date to 2016-01-17"

class ActivityModelAdmin(VersionAdmin):
    ordering = ('-date', )
    actions = [activity_change_date]

admin.site.register(Member, MemberModelAdmin)
admin.site.register(Activity, ActivityModelAdmin)
