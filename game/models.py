# encoding: utf-8
from django.db.models import *
from namebook.models import Entity

class Tournament(Model):
    "一次赛事，由许多场比赛Match组成"

    TOURNAMENT_TYPES= (
            (1, "单淘汰"),
            (2, "单循环"),
            )

    name = CharField(max_length=50)
    type = IntegerField(choices=TOURNAMENT_TYPES, null=True)
    #participants
    text = TextField(blank=True)


class Match(Model):
    "一场比赛，通常为三局两胜制"

    MATCH_TYPES = (
            (1, "男单"),
            (2, "女单"),
            (3, "男双"),
            (4, "女双"),
            (5, "混双"),
            )

    tournament = ForeignKey(Tournament)
    type = IntegerField(choices=MATCH_TYPES)
    result = IntegerField(null=True) # 比赛结果，1,2代表赢家
    player1a = ForeignKey(Entity, related_name="player1a")
    player1b = ForeignKey(Entity, null=True, related_name="player1b")
    player2a = ForeignKey(Entity, related_name="player2a")
    player2b = ForeignKey(Entity, null=True, related_name="player2b")
    datetime = DateTimeField(null=True)
    extra = TextField(blank=True) # json record


    def __unicode__(self):
        p1 = unicode(self.player1a.name)
        if self.player1b:
            p1 += u" " + unicode(self.player1b.name)
        p2 = unicode(self.player2a.name)
        if self.player2b:
            p2 += u" " + unicode(self.player2b.name)

        if result == 1:
            return p1 + u" 胜 " + p2
        else:
            return p2 + u" 胜 " + p1


class Game(Model):
    "一局比赛，通常为21分制"
    match = ForeignKey(Match)
    score1 = IntegerField()
    score2 = IntegerField()
    extra = TextField(blank=True) # json record

    def __unicode__(self):
        return u"%d:%d" % (self.score1, self.score2)

