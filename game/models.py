# encoding: utf-8
from django.db.models import *
from namebook.models import Entity
import parser

class Extension:
    def xget(self, key):
        return json.loads(self.extra)[key]

    def xset(self, key, val):
        r = json.loads(self.extra)
        r[key] = val
        self.extra = json.dumps(r)

class Tournament(Model, Extension):
    "一次赛事，由许多场比赛Match组成"

    TOURNAMENT_TYPES= (
            (1, "单淘汰"),
            (2, "单循环"),
            )

    name = CharField(max_length=50)
    type = IntegerField(choices=TOURNAMENT_TYPES, null=True)
    participants = ManyToManyField(Entity)
    text = TextField(blank=True)
    extra = TextField(default="{}") # json record

    def __unicode__(self):
        return u"%s" %(name)

    def addMatch(self, source):
        return parser.parseMatch(source, self)

    def get_or_add_participant(self, name):
        p = self.participants.filter(name__exact=name)
        if p:
            return p[0]
        else:
            p = Entity.objects.create(name=name)
            self.participants.add(p)
            return p

class Match(Model, Extension):
    "一场比赛，通常为三局两胜制"

    tournament = ForeignKey(Tournament, null=True)
    result = IntegerField(null=True) # 比赛结果，1,2代表赢家
    player1a = ForeignKey(Entity, related_name="player1a")
    player1b = ForeignKey(Entity, null=True, related_name="player1b")
    player2a = ForeignKey(Entity, related_name="player2a")
    player2b = ForeignKey(Entity, null=True, related_name="player2b")
    comment = TextField(blank=True)
    extra = TextField(default="{}") # json record

    def __unicode__(self):
        p1 = unicode(self.player1a.name)
        if self.player1b:
            p1 += u" " + unicode(self.player1b.name)
        p2 = unicode(self.player2a.name)
        if self.player2b:
            p2 += u" " + unicode(self.player2b.name)

        if self.result == 1:
            p= p1 + u" 胜 " + p2
        elif self.result == 2:
            p= p1 + u" 负 " + p2
        else:
            p= p1 + u" 对 " + p2

        scores = " ".join([unicode(game) for game in self.game_set.all()])
        return p+" " + scores + "\n" + self.comment


class Game(Model, Extension):
    "一局比赛，通常为21分制"
    match = ForeignKey(Match)
    score1 = IntegerField()
    score2 = IntegerField()
    extra = TextField(default="{}") # json record

    def __unicode__(self):
        return u"%d:%d" % (self.score1, self.score2)

