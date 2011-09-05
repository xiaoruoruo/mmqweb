from django.db.models import *

class GameRecord(Model):
    ip = CharField(max_length=40)
    json = CharField(max_length=1000)
    
