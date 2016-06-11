# encoding: utf-8
import itertools
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from club.models import Member, Activity
from reversion import revisions as reversion
import club.admin  # for registration of reversion

class Command(BaseCommand):
    help = 'Check duplicate checkins for each day.'

    @transaction.atomic
    def handle(self, *args, **options):
        with reversion.create_revision():
            assert self.check_duplicate()
            reversion.set_comment("Check duplicate")
        print "Run checkbalance afterwards."

    def check_duplicate(self):
        success = True
        all_acts = Activity.objects.order_by('date').select_related('member')
        for date, acts in itertools.groupby(all_acts, lambda a: a.date):
            if date.year < 2016: continue
            today = {}
            for a in acts:
                if a.member in today:
                    if today[a.member] == (a.cost, a.deposit):
                        # remove duplicate
                        print u"Duplicate checkin for {0} on {1}".format(a.member.name, date)
                        a.delete()
                    elif self.compatible(today[a.member], (a.cost, a.deposit)):
                        pass
                    else:
                        # not really duplicate
                        print u"Multiple checkins for {0} on {1}: ({2} {3}) ({4} {5})".format(
                            a.member.name, date, today[a.member][0], today[a.member][1], a.cost, a.deposit)
                        success = False
                else:
                    today[a.member] = (a.cost, a.deposit)
        return success

    def compatible(self, ta, tb):
        t = lambda x: x is None or x == 0.0
        return (t(ta[0]) and t(tb[1])) or (t(ta[1]) and t(tb[0]))

