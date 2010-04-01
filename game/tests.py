# encoding: utf-8
from django.test import TestCase
from namebook.models import *
from game.models import *
from game import parser
from game import ranker

class SimpleTest(TestCase):
    def setUp(self):
        self.mmqtao=Entity.objects.create(name=u"套长")
        self.redwolf=Entity.objects.create(name=u"老大")

        t=Tournament.objects.create(name=u"测试赛", type=1)
        self.t = t

        t.add_participant(self.mmqtao, None, None)
        t.add_participant(self.redwolf, None, None)
        self.assertEquals(2, self.t.participants.count())


    def test1(self):
        m=self.t.addMatch(u'''老大:套长 21：19 12：21 21：12
上面一行格式固定，这一行可以写评论。用[耗时:10]来表示结构化的数据。弃权，犯规等导致胜方需要特别说明的情况，在这里用[胜者:老大]表示。''')

        self.assertEquals(self.t, m.tournament)
        self.assertTrue(len(m.text) > 10)
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

        self.assertEquals(result, self.t.ranking())

class Tizong(TestCase):
    teams = ["电子信息与电气工程学院","农业与生物学院","国际教育学院","理学院物理系","生命科学技术学院",
             "外国语学院","环境科学与工程学院","交大密西根学院","软件学院","航空航天学院",
             "船舶海洋与建筑工程","药学院","信息安全工程学院","医学院","法学院",
             "材料科学与工程学院","微电子学院","机械与动力工程学院","媒体与设计学院","化学化工学院",
             "理学院数学系"]

    def test1(self):
        teamsE = []
        for team in self.teams:
            teamsE.append(Entity.objects.create(name=team, type=Entity.Team))
        self.assertEquals(21, Entity.objects.filter(type=Entity.Team).count()) # 21 teams

        t = []
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛A组", type=2))
        t[-1].set_ranking_targets(teamsE[0:4])
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛B组", type=2))
        t[-1].set_ranking_targets(teamsE[4:8])
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛C组", type=2))
        t[-1].set_ranking_targets(teamsE[8:13])
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛D组", type=2))
        t[-1].set_ranking_targets(teamsE[13:17])
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛E组", type=2))
        t[-1].set_ranking_targets(teamsE[17:21])

class RealTeamMatch(TestCase):
    "http://www.tournamentsoftware.com/sport/teammatch.aspx?id=991DFE99-023B-4853-8AF6-39255247D465&match=12"
    def test(self):
        return
        team1 = Entity.objects.create(name="Malaysia", type=Entity.Team)
        team2 = Entity.objects.create(name="Korea", type=Entity.Team)
        kkk = Entity.objects.create(name="Kean Keat Koo", type=Entity.Man)
        ptw = Entity.objects.create(name="Pei Tty Wong", type=Entity.Woman)
        
        match1 = Match.objects.create()
        match1.player1 = Participation.objects.create(playera = team1)
        match1.player2 = Participation.objects.create(playera = team2)
        match1.result = 2

        match11 = Match.objects.create()
        match11.player1 = Participation.objects.create(playera = kkk, playerb = ptw, represent=team1)
