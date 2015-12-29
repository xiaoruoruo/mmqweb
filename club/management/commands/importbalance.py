import io
from django.core.management.base import BaseCommand, CommandError
from club.models import Member, Activity
from django.db.transaction import atomic
from reversion import revisions as reversion
import club.admin  # for registration of reversion
from datetime import datetime
import pdb

class Command(BaseCommand):
    @atomic
    def handle(self, *args, **options):
        f = io.open(args[0], 'r', encoding='utf8')
        date = datetime.strptime(args[1], "%Y-%m-%d")
        comment = unicode(args[2], 'utf8')

        with reversion.create_revision():
            self.do_import(f, date, comment)
            reversion.set_comment(u"Import balance: %s" % comment)

    def do_import(self, f, date, comment):
        for line in f:
            name, balance = line[:-1].split(',')
            balance = float(balance)
            try:
                member = Member.objects.get(name=name, hidden=False)
                a = Activity(
                        member  = member,
                        weight  = 0.0,
                        date    = date,
                        cost    = -balance if balance < 0 else 0,
                        deposit = balance  if balance > 0 else 0,
                        comment = comment,
                        )
                a.save()

                acts, running, sum = member.running_total()
                if sum != member.balance:
                    member.balance = sum
                    member.save()

            except Member.DoesNotExist:
                ms = list(Member.objects.filter(name=name))
                if len(ms) == 0:
                    print name, "Not found"
                elif len(ms) == 1:
                    if ms[0].hidden:
                        print name, "is hidden"
                    else:
                        assert False
                else:
                    assert False
        f.close()

