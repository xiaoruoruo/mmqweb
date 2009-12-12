# encoding: utf-8
from django.test import TestCase
from namebook.models import *
from game.models import *
from game import parser
from game import ranker

class SimpleTest(TestCase):
    def setUp(self):
        self.mmqtao=Entity.objects.create(name=u"套长")

        t=Tournament.objects.create(name=u"测试赛")
        t.participants.add(self.mmqtao)

        self.t = t

    def test1(self):
        m=self.t.addMatch(u'''老大:套长 21：19 12：21 21：12
上面一行格式固定，这一行可以写评论。用[耗时:10]来表示结构化的数据。弃权，犯规等导致胜方需要特别说明的情况，在这里用[胜者:老大]表示。''')

        self.assertEquals(self.t, m.tournament)
        self.assertEquals(2, self.t.participants.count())
        self.assertTrue(len(m.comment) > 10)
        self.redwolf = m.player1a
        self.assertEquals(u"老大", self.redwolf.name)
        self.assertEquals(self.mmqtao, m.player2a)
        self.assertEquals(None, m.player1b)
        self.assertEquals(None, m.player2b)
        self.assertEquals(1, m.winner()) # player1 wins

        games = m.game_set.all()
        self.assertEquals(3, games.count())

        self.assertEquals(u'''老大 胜 套长 21:19 12:21 21:12
上面一行格式固定，这一行可以写评论。用[耗时:10]来表示结构化的数据。弃权，犯规等导致胜方需要特别说明的情况，在这里用[胜者:老大]表示。''', unicode(m))

    def test2(self):
        self.test1()
        self.assertEquals(1, self.t.match_set.count())
        
        rank = ranker.RoundRobinRanker([self.redwolf, self.mmqtao], self.t.match_set.all())
        result = rank.result()
        self.assertEquals(2, len(result))
        self.assertEquals(1, result[0][0])
        self.assertEquals(self.redwolf, result[0][1])
        self.assertEquals(2, result[1][0])
        self.assertEquals(self.mmqtao, result[1][1])
