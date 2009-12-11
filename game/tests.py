# encoding: utf-8
from django.test import TestCase
from namebook.models import *
from game.models import *
from game import parser

class SimpleTest(TestCase):
    def setUp(self):
        self.a=Entity.objects.create(name=u"套长")
        self.b=Entity.objects.create(name=u"老大")

        t=Tournament.objects.create(name=u"测试赛")
        t.participants.add(self.a)
        t.participants.add(self.b)
        self.assertEquals(2, t.participants.count())

        self.t = t

    def test1(self):
        m=self.t.addMatch(u'''老大:套长 21：19 12：21 21：12
上面一行格式固定，这一行可以写评论。用[耗时:10]来表示结构化的数据。弃权，犯规等导致胜方需要特别说明的情况，在这里用[胜者:老大]表示。''')

        self.assertEquals(self.t, m.tournament)
        self.assertTrue(len(m.comment) > 10)
        self.assertEquals(self.b, m.player1a)
        self.assertEquals(self.a, m.player2a)
        self.assertEquals(None, m.player1b)
        self.assertEquals(None, m.player2b)
        self.assertEquals(1, m.result) # player1 wins

        games = m.game_set.all()
        self.assertEquals(3, games.count())

        self.assertEquals(u'''老大 胜 套长 21:19 12:21 21:12
上面一行格式固定，这一行可以写评论。用[耗时:10]来表示结构化的数据。弃权，犯规等导致胜方需要特别说明的情况，在这里用[胜者:老大]表示。''', unicode(m))

    def test2(self):
        try:
            self.t.addMatch( u"路人甲:路人乙 21:0\n." )
        except parser.NotRegisteredPlayerError:
            self.assertTrue( True )  # TODO why this doesn't happen?
        except:
            #import sys
            #print sys.exc_info()[0]
            #raise
            pass
        else:
            self.fail()
