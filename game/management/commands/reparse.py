from django.core.management.base import BaseCommand, CommandError
from mmqweb.game.models import *
from mmqweb.game.parser import updateText

class Command(BaseCommand):
    def handle(self, *args, **options):
        for match in Match.objects.all():
            s = unicode(match)
            text = s.split(u"\n",1)[1]
            updateText(match, text)
            match.save()
