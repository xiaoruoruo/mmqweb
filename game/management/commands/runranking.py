from django.core.management.base import BaseCommand, CommandError
from mmqweb.game.models import *
from mmqweb.game.ranker import NaiveRanker

class Command(BaseCommand):
    def handle(self, *args, **options):
        mg = MatchGroup.objects.get(id=1)
        ranker = NaiveRanker([], mg.match_set.all())
