from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from club.models import Member, Activity
import reversion
import club.admin  # for registration of reversion

DROP_PER_MONTH = 0.5

class Command(BaseCommand):
    @transaction.commit_on_success
    def handle(self, *args, **options):
        with reversion.create_revision():
            self.update_weight_for_all()
            reversion.set_comment("Update weight")

    def update_weight_for_all(self):
        lastmonth = None
        members = list(Member.objects.all())
        self.karma = dict((m,0.0) for m in members)

        acts = Activity.objects.order_by('date')
        for a in acts:
            month = a.date.toordinal() / 30
            if lastmonth is None:
                lastmonth = month
            if lastmonth < month:
                self.demote(month - lastmonth)
                lastmonth = month
            if a.weight > 0:
                self.promote(a.member)

        for member in self.karma:
            if member.weight != self.karma[member]:
                member.weight = self.karma[member]
                member.save()

    def promote(self, member):
        self.karma[member] += 1

    def demote(self, months):
        eff = pow(DROP_PER_MONTH, months)
        for member in self.karma:
            self.karma[member] *= eff
