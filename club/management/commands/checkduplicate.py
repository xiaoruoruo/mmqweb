import itertools
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from club.models import Member, Activity
import reversion
import club.admin  # for registration of reversion

class Command(BaseCommand):
    help = 'Check duplicate checkins for each day.'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        with reversion.create_revision():
            self.check_duplicate()
            reversion.set_comment("Check duplicate")
        print "Run checkbalance afterwards."

    def check_duplicate(self):
        all_acts = Activity.objects.order_by('date').select_related('member')
        for date, acts in itertools.groupby(all_acts, lambda a: a.date):
            today = {}
            for a in acts:
                if a.member in today:
                    if today[a.member] == (a.cost, a.deposit):
                        # remove duplicate
                        print "Duplicate checkin for %s on %s" % (a.member.name, date)
                        a.delete()
                    else:
                        # not really duplicate
                        print "Multiple checkins for %s on %s: (%.2f %.2f) (%.2f %.2f)" \
                            % (a.member.name, date, a.cost, a.deposit, a.cost, a.deposit)
                        assert False
                else:
                    today[a.member] = (a.cost, a.deposit)

