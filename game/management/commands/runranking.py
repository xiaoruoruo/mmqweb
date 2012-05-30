# encoding: utf8
from django.core.management.base import BaseCommand, CommandError
from mmqweb.game.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        for ranking in Ranking.objects.all():
            print ranking.name
            ranker = ranking.get_ranker()
            ranker.rank()
            print ranker.print_by_type(Entity.Man),
            print ranker.print_by_type(Entity.Woman),

