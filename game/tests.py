# encoding: utf-8
from django.test import TestCase
from namebook.models import *
from game.models import *
from game import parser
from game import ranker

import random

class SimpleTest(TestCase):
    def setUp(self):
        self.mmqtao=Entity.objects.create(name=u"套长")
        self.redwolf=Entity.objects.create(name=u"老大")

        t=Tournament.objects.create(name=u"测试赛")
        self.t = t
        self.g=MatchGroup.objects.create(name=u"",tournament=t)

        t.add_participant(self.mmqtao, None, None)
        t.add_participant(self.redwolf, None, None)
        self.assertEquals(2, self.t.participants.count())


    def test1(self):
        m=self.g.addMatch(u'''老大:套长 21：19 12：21 21：12
上面一行格式固定，这一行可以写评论。用[耗时:10]来表示结构化的数据。弃权，犯规等导致胜方需要特别说明的情况，在这里用[胜者:老大]表示。''')
        self.m = m

        self.assertEquals(self.t, m.match_group.tournament)
        self.assertTrue(len(m.text) > 10)
        self.assertEquals(1, m.winner()) # player1 wins

        games = m.game_set.all()
        self.assertEquals(3, games.count())

        self.assertEquals(u'''老大 胜 套长 21:19 12:21 21:12
上面一行格式固定，这一行可以写评论。用[耗时:10]来表示结构化的数据。弃权，犯规等导致胜方需要特别说明的情况，在这里用[胜者:老大]表示。''', unicode(m))

    def test2(self):
        self.test1()

        rank = ranker.RoundRobinRanker([self.redwolf, self.mmqtao], self.g.match_set.all())
        result = rank.result()
        self.assertEquals(2, len(result))
        self.assertEquals(1, result[0][0])
        self.assertEquals(self.redwolf, result[0][1])
        self.assertEquals(2, result[1][0])
        self.assertEquals(self.mmqtao, result[1][1])

    def testExtra(self):
        self.test1()
        self.assertEquals(u'10', self.m.xget(u'耗时'))
        self.assertEquals(u'老大', self.m.xget(u'胜者'))

    def testSort(self):
        m1=self.g.addMatch(u'''老大:套长 21：1\n[时间:2012年03月01日]''')
        m2=self.g.addMatch(u'''老大:套长 21：2\n[时间:2012年03月02日]''')
        self.assertTrue(m1 < m2)
        ms = [m2,m1]
        ms.sort()
        self.assertEquals([m1, m2], ms)

    def testParser(self):
        from parser import ParseError
        self.assertRaises(ParseError, self.g.addMatch, u'A:B 21:12 12:2121:12')

    def testOneVsTwo(self):
        m = self.g.addMatch(u'''小小 龟龟：fish 13:20''')
        self.assertEquals(2, m.winner())
        self.assertEquals(Match.OneVsTwo, m.type)



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
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛A组"))
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛B组"))
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛C组"))
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛D组"))
        t.append(Tournament.objects.create(name=u"2010年体总杯羽毛球赛小组赛E组"))

class VirtualTournament:
    def test(self):
        t = Tournament.objects.create(name=u"Virtual Tournament")
        tg = MatchGroup.objects.create(name=u"The Group", tournament = t, view_name = "roundrobin")
        r = Ranking.objects.create(name = "Virtual Ranking", type = 2, mg = tg)

        teams = []
        for i in range(4):
            teams.append( Entity.objects.create(name="Team %d" % i, type=Entity.Team) )

        player_count = 0
        teamplayer = []
        for team in teams:
            players = []
            for i in range(8): # 8 participants per team
                p = Entity.objects.create(name="Player %d" % player_count)
                player_count += 1
                t.add_participant(p, team)
                players.append(p)
            teamplayer.append(players)

        mss = []
        for i in range(4):
            for j in range(i+1,4):
                # team i vs team j
                ms = []
                for k in range(2):
                    m = Match()
                    m.match_group = tg
                    m.player11 = teamplayer[i][k]
                    m.player21 = teamplayer[j][k]
                    m.result = random.randint(1,2)
                    m.save()
                    ms.append(m)
                for k in range(3):
                    m = Match()
                    m.match_group = tg
                    m.player11 = teamplayer[i][2+k*2]
                    m.player12 = teamplayer[i][3+k*2]
                    m.player21 = teamplayer[j][2+k*2]
                    m.player22 = teamplayer[j][3+k*2]
                    m.result = random.randint(1,2)
                    m.save()
                    ms.append(m)
                for m in ms:
                    g = Game()
                    g.match = m
                    if m.result == 1:
                        g.score1, g.score2 = 21, random.randint(0,20)
                    else:
                        g.score2, g.score1 = 21, random.randint(0,20)
                    g.save()
                mss.extend(ms)

        for i,e,s in r.ranking():
            print i,e,s
            pass

class VirtualTournamentTest(VirtualTournament,TestCase):
    pass

class PersonalRankingTest(TestCase):
    def setUp(self):
        self.t = t = Tournament.objects.create(name=u"Personal Tournament")
        self.tg = tg = MatchGroup.objects.create(name=u"The Group", tournament = t, view_name = "roundrobin")
        self.r = Ranking.objects.create(name = "Ranking", type = 4, mg = tg)

        matches = [
            u'老大:套长 21：1\n[时间:2012年03月01日]',
            u'老大:fish 1：21\n[时间:2012年03月02日]',
            u'老大、猪头:fish、鱼头 21：1\n[时间:2012年03月02日]',
            u'老大、fish:鱼头、猪头 21：1\n[时间:2012年03月02日]',
                ]
        for m in matches:
            self.tg.addMatch(m)

        self.assertEquals(len(matches), self.tg.match_set.count())

    def testElo(self):
        from game.ranker import EloPersonalRanker
        ranker = EloPersonalRanker(self.r)
        ranker.rank()
        #for r in PersonalRating.objects.all():
        #    print r
        self.assertEquals(12, PersonalRating.objects.count())
        rating_laoda = ranker.rating(
            Entity.objects.get(name=u'老大')).rating_singles
        rating_fish = ranker.rating(
            Entity.objects.get(name=u'fish')).rating_singles
        rating_doubles_laoda = ranker.rating(
            Entity.objects.get(name=u'老大')).rating_doubles
        rating_doubles_zhutou = ranker.rating(
            Entity.objects.get(name=u'猪头')).rating_doubles
        self.assertTrue(rating_fish > rating_laoda)
        self.assertTrue(rating_doubles_laoda > rating_doubles_zhutou)

    def testFish(self):
        from game.ranker import FishPersonalRanker
        ranker = FishPersonalRanker(self.r)
        ranker.rank()
        # for r in PersonalRating.objects.all():
        #     print r
        self.assertEquals(12, PersonalRating.objects.count())
        self.assertEquals(4.0, ranker.rating(
            Entity.objects.get(name=u'老大')).rating_singles)
        self.assertEquals(3.0, ranker.rating(
            Entity.objects.get(name=u'fish')).rating_singles)

class PersonalRankingOneVsTwoTest(TestCase):
    def setUp(self):
        self.t = t = Tournament.objects.create(name=u"Personal Tournament")
        self.tg = tg = MatchGroup.objects.create(name=u"The Group", tournament = t, view_name = "roundrobin")
        self.r = Ranking.objects.create(name = "Ranking", type = 4, mg = tg)

        matches = [
                u'''小小 龟龟：fish 13:20''',
                ]
        for m in matches:
            self.tg.addMatch(m)

    def tearDown(self):
        self.ranker.rank()
        ranker = self.ranker
        # for r in PersonalRating.objects.all():
        #     print r
        self.assertEquals(None, ranker.rating(Entity.objects.get(name=u'fish')).rating_doubles)
        self.assertEquals(None, ranker.rating(Entity.objects.get(name=u'小小')).rating_singles)
        self.assertEquals(None, ranker.rating(Entity.objects.get(name=u'龟龟')).rating_singles)
        self.assertTrue(ranker.rating(Entity.objects.get(name=u'fish')).rating_singles >
                ranker.rating(Entity.objects.get(name=u'小小')).rating_doubles)
        self.assertTrue(ranker.rating(Entity.objects.get(name=u'fish')).rating_singles >
                ranker.rating(Entity.objects.get(name=u'龟龟')).rating_doubles)

    def testFish(self):
        from game.ranker import FishPersonalRanker
        self.ranker = FishPersonalRanker(self.r)

    def testElo(self):
        from game.ranker import EloPersonalRanker
        self.ranker = EloPersonalRanker(self.r)
