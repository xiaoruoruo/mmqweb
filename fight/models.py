from django.db.models import *
import json

class GameRecord(Model):
    ip = CharField(max_length=40)
    json = CharField(max_length=1000)
    
    def __unicode__(self):
        o = json.loads(self.json)
        if o['ver'] >= 1:
            duration = (o['endTime'] - o['readyTime'])/1000.0/60.0
        return "%f min" % duration

