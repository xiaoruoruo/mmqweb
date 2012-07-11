import io
from django.core.management.base import BaseCommand, CommandError
from club.models import Member

class Command(BaseCommand):
    def handle(self, *args, **options):
        f = io.open(args[0], 'r', encoding='utf8')
        male = args[1]=='True'
        for line in f:
            name, w = line[:-1].split(' ')
            m = Member(name=name, weight=w, male=male)
            m.save()
        f.close()

