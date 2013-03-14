from club.models import Member, Activity
from django.contrib import admin
import reversion

class MemberModelAdmin(reversion.VersionAdmin):
    list_display = ('name', 'sex', 'balance', 'weight')
    ordering = ('-weight', )

class ActivityModelAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Member, MemberModelAdmin)
admin.site.register(Activity, ActivityModelAdmin)
