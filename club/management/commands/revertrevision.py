from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from club.models import Member, Activity
import reversion
from reversion.models import Revision
import club.admin  # for registration of reversion

class Command(BaseCommand):
    args = '<revision_id revision_id ...>'
    help = 'Revert new activities created in selected revisions, and revert the balances.'

    activity_type = ContentType.objects.get(app_label="club", model="activity")
    @transaction.atomic
    def handle(self, *args, **options):
        with reversion.create_revision():
            for revision_id in args:
                self.revert_revision(int(revision_id))
            reversion.set_comment("Revert revisions: " + ",".join(args))

    def revert_revision(self, revision_id):
        r = Revision.objects.get(id=revision_id)
        for v in r.version_set.filter(content_type=self.activity_type):
            act = v.object
            member = act.member
            member.balance += act.cost
            if act.deposit:
                member.balance -= act.deposit
            member.save()
            act.delete()


