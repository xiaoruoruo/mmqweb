from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from club.models import Member, Activity
import reversion
import club.admin  # for registration of reversion

class Command(BaseCommand):
    help = 'Check the balance for each member and reset the balance if wrong.'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        with reversion.create_revision():
            self.check_balance()
            reversion.set_comment("Check balance")

    def check_balance(self):
        for member in Member.objects.all():
            acts, running, sum = member.running_total()
            if sum != member.balance:
                print "%s balance is %.2f should be %.2f" % \
                    (member.name, member.balance, sum)
                member.balance = sum
                member.save()

