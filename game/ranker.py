# encoding: utf-8
from itertools import groupby
from django.db import transaction
from django.db.models import Max

from namebook.models import Entity
from game.models import PersonalRating

class Ranker:
    def __init__(self, targets, matches):
        """
        targets: target列表，每个target为一个Entity对象（单打，团体）或Entity tuple（双打）
        """
        raise NotImplementedError
    def result(self):
        "返回排好序的序列[(rank, target, comment), ...]"
        raise NotImplementedError

class PersonalRanker(Ranker):
    def __init__(self, ranking):
        self.ranking = ranking
        self.mg = ranking.mg
        self.matches = sorted(self.mg.match_set.all())

    @transaction.commit_on_success
    def rank(self):
        """
        删除所有rating，重新排
        """
        PersonalRating.objects.filter(ranking=self.ranking).delete()
        for m in self.matches:
            self.update(m)

    def rating(self, player):
        "查询rating"
        return PersonalRating.objects.filter(ranking=self.ranking,
                player=player).order_by('-id')[0]

    def update(self, match):
        "match发生后更新相应排名"
        raise NotImplementedError

    def print_by_type(self, type):
        "输出所有最新积分"
        def run(sd):
            subq = PersonalRating.objects.filter(ranking=self.ranking, player__type=type).values('player__id').annotate(Max('id')).values_list('id__max',flat=True)
            rating_field = 'rating_%s' % sd
            es = PersonalRating.objects.filter(id__in=subq).order_by('-'+rating_field).values_list('player__name', rating_field)
            return '\n'.join("%s %.2f" % (name, rating) for name, rating in es if rating) + '\n' + '\n'

        s = u""
        s += Entity.ENTITY_TYPES_DICT[type] + u" "
        s += u"单打\n"
        s += run('singles')

        s += Entity.ENTITY_TYPES_DICT[type] + u" "
        s += u"双打\n"
        s += run('doubles')
        return s


class FishPersonalRanker(PersonalRanker):
    INIT_RATING = 0
    def update(self, m):
        w = m.winner()
        if not m.player12: # is singles
            self._update(m, m.player11, 3 if w == 1 else 1, 'singles')
            self._update(m, m.player21, 3 if w == 2 else 1, 'singles')
        else:
            self._update(m, m.player11, 3 if w == 1 else 1, 'doubles')
            self._update(m, m.player12, 3 if w == 1 else 1, 'doubles')
            self._update(m, m.player21, 3 if w == 2 else 1, 'doubles')
            self._update(m, m.player22, 3 if w == 2 else 1, 'doubles')

    def _update(self, match, player, amount, kind):
        pr = PersonalRating.objects.filter(ranking=self.ranking,
                player=player).order_by('-id')[:1]
        s = {}
        if pr:
            pr = pr[0]
            s['singles']= pr.rating_singles
            s['doubles']= pr.rating_doubles
        if kind not in s or s[kind] is None:
            s[kind] = self.INIT_RATING
        s[kind] += amount
        pr = PersonalRating.objects.create(player=player, match=match,
                ranking=self.ranking,
                rating_singles = s.get('singles',None),
                rating_doubles = s.get('doubles',None),
                )
        pr.save()

class EloPersonalRanker(PersonalRanker):
    INIT_RATING = 1200
    def update(self, m):
        w = m.winner()
        if not m.player12: # is singles
            self._update2(m, m.player11, m.player21) if w == 1 else self._update2(m, m.player21, m.player11)
        else:
            if w == 1:
                self._update4(m, m.player11, m.player12, m.player21, m.player22)
            else:
                self._update4(m, m.player21, m.player22, m.player11, m.player12)

    def getPlayerRating(self, player): # get player rating
        pr = PersonalRating.objects.filter(ranking = self.ranking,
                player = player).order_by('-id')[:1]
        s = {}
        if pr:
            pr = pr[0]
            s['singles'] = pr.rating_singles
            s['doubles'] = pr.rating_doubles
        return s

    def savePlayerRating(self, player, rating, match): # save player rating
        pr = PersonalRating.objects.create(player=player, match=match,
                ranking=self.ranking,
                rating_singles = rating.get('singles',None),
                rating_doubles = rating.get('doubles',None),
                )
        pr.save()
        return

    def _update2(self, match, playerA, playerB):
        ratingA = self.getPlayerRating(playerA)
        ratingB = self.getPlayerRating(playerB)
        for r in [ratingA, ratingB]:
            if r.get('singles', None) is None:
                r['singles'] = self.INIT_RATING

        newRatingA, newRatingB  = self.updateRank(ratingA['singles'], ratingB['singles'])

        ratingA['singles'] = newRatingA
        ratingB['singles'] = newRatingB
        self.savePlayerRating(playerA, ratingA, match)
        self.savePlayerRating(playerB, ratingB, match)
        return

    def _update4(self, match, playerA1, playerA2, playerB1, playerB2):
        ratingA1 = self.getPlayerRating(playerA1)
        ratingA2 = self.getPlayerRating(playerA2)
        ratingB1 = self.getPlayerRating(playerB1)
        ratingB2 = self.getPlayerRating(playerB2)
        for r in [ratingA1, ratingA2, ratingB1, ratingB2]:
            if r.get('doubles', None) is None:
                r['doubles'] = self.INIT_RATING

        groupRatingA = (ratingA1['doubles'] + ratingA2['doubles']) / 2
        groupRatingB = (ratingB1['doubles'] + ratingB2['doubles']) / 2

        newGroupRatingA, newGroupRatingB  = self.updateRank(groupRatingA, groupRatingB)

        groupRatingUpdateA = newGroupRatingA - groupRatingA;
        ratingUpdateA1 = groupRatingUpdateA * ratingA2['doubles'] / (ratingA1['doubles'] + ratingA2['doubles'])
        ratingUpdateA2 = groupRatingUpdateA - ratingUpdateA1;

        groupRatingUpdateB = newGroupRatingB - groupRatingB;
        ratingUpdateB1 = groupRatingUpdateB * ratingB2['doubles'] / (ratingB1['doubles'] + ratingB2['doubles'])
        ratingUpdateB2 = groupRatingUpdateB - ratingUpdateB1;

        ratingA1['doubles'] += ratingUpdateA1
        ratingA2['doubles'] += ratingUpdateA2
        ratingB1['doubles'] += ratingUpdateB1
        ratingB2['doubles'] += ratingUpdateB2

        self.savePlayerRating(playerA1, ratingA1, match)
        self.savePlayerRating(playerB1, ratingB1, match)
        self.savePlayerRating(playerA2, ratingA2, match)
        self.savePlayerRating(playerB2, ratingB2, match)
        return

    def updateRank(self, ratingA, ratingB): # assume A is winner
        expectionScoreForA = 1.0 / (1.0 + pow(10.0, (ratingB - ratingA) / 400))
        K = 50 # maximum rating change
        ratingDelta = (1.0 - expectionScoreForA) * K
        newRatingA = ratingA + ratingDelta
        newRatingB = ratingB - ratingDelta
        return [newRatingA, newRatingB]


class RoundRobinRanker(Ranker):
    stats_template = {'match_win':0, 'game_win':0, 'game_lose':0,'score_win':0, 'score_lose':0}
    def find_target(self, a, add=False):
        "given Participation a, return an object in targets"
        if a in self.target_points:
            return a
        elif add:
            self.target_points[a] = dict(RoundRobinRanker.stats_template)
            return a
        else:
            print u"玩家不属于任何积分组",
            print a
            raise ValueError()  # how to raise unicode Exception?

    def __init__(self, targets, matches):
        if targets is not None:
            p = dict((target, dict(RoundRobinRanker.stats_template)) for target in targets)
            add = False
        else:
            p={}
            add = True

        self.target_points=p
        self.matches = {}
        for match in matches:
            t1 = self.find_target(match.get_target(1), add)
            t2 = self.find_target(match.get_target(2), add)
            w = match.winner()
            target_pair, score_i = (t1,t2), 0
            if target_pair not in self.matches:
                if (t2,t1) in self.matches:
                    target_pair,score_i = (t2,t1), 1
                else:
                    self.matches[(t1, t2)] = [0,0]
            #print t1,"VS",t2,w
            if w==1:
                p[t1]['match_win'] += 1
                self.matches[target_pair][score_i] += 1
            elif w==2:
                p[t2]['match_win'] += 1
                self.matches[target_pair][1-score_i] += 1

            for game in match.game_set.all():
                if game.winner()==1:
                    p[t1]['game_win'] += 1
                    p[t2]['game_lose'] += 1
                elif game.winner()==2:
                    p[t2]['game_win'] += 1
                    p[t1]['game_lose'] += 1
                p[t1]['score_win'] += game.score1
                p[t1]['score_lose'] += game.score2
                p[t2]['score_lose'] += game.score1
                p[t2]['score_win'] += game.score2
        #print p

    def result(self):
        result = []
        board = list(self.target_points.keys())
        #获胜场数多者名次在前
        match_list = give_rank(board, self.cmp_match, 1)
        for rank, g in groupby(match_list, lambda x:x[0]):
            g=list(g)
            match_win = self.target_points[g[0][1]]['match_win']
            str_match = u"获胜场数:%d" % match_win
            if len(g)==1:
                result.append((rank, g[0][1], str_match))
            elif len(g)==2:
                #两名（对）运动员获胜场数相等，则两者比赛的胜者名次列前
                a, b = give_rank([x[1] for x in g], self.cmp_winner, rank)
                result.append((a[0], a[1], str_match))
                result.append((b[0], b[1], str_match))
            else:
                #3名（对）或3名（对）以上运动员获胜场数相等，则按在该组比赛的净胜局数定名次
                game_list = give_rank([x[1] for x in g], self.cmp_game, rank)
                for rank1, g1 in groupby(game_list, lambda x:x[0]):
                    g1=list(g1)
                    game_delta = self.target_points[g1[0][1]]['game_win'] - self.target_points[g1[0][1]]['game_lose']
                    str_game = u"%s，净胜局:%d" % (str_match, game_delta)
                    if len(g1)==1:
                        result.append((rank1, g1[0][1], str_game))
                    elif len(g1)==2:
                        #两名（对）运动员净胜局数相等，则两者比赛的胜者名次列前
                        a, b = give_rank([x[1] for x in g1], self.cmp_winner, rank1)
                        result.append((a[0], a[1], str_game))
                        result.append((b[0], b[1], str_game))
                    else:
                        #还剩3名（对）或3名（对）以上运动员净胜局数相等，则按在该组比赛的净胜分数定名次
                        score_list = give_rank([x[1] for x in g1], self.cmp_score, rank1)
                        for rank2, g2 in groupby(score_list, lambda x:x[0]):
                            g2=list(g2)
                            score_delta = self.target_points[g2[0][1]]['score_win'] - self.target_points[g2[0][1]]['score_lose']
                            str_score = u"%s，净胜分:%d" % (str_game, score_delta)
                            if len(g2)==1:
                                result.append((rank2, g2[0][1], str_score))
                            elif len(g2)==2:
                                #如还剩2名（对）运动员净胜分数相等，则两者间比赛的胜者名次列前
                                a, b = give_rank([x[1] for x in g2], self.cmp_winner, rank2)
                                result.append((a[0], a[1], str_score))
                                result.append((b[0], b[1], str_score))
                            else:
                                #真的比不出来了
                                for g2i in g2:
                                    result.append((g2i[0], g2i[1], u"并列, %s" % str_score))

        return result

    def cmp_winner(self, a, b):
        # a胜b返回-1，b胜a返回1
        if (a, b) in self.matches:
            w=self.matches[(a, b)]
            if w[0]>w[1]:
                return -1
            elif w[0]<w[1]:
                return 1
        elif (b, a) in self.matches:
            w=self.matches[(b, a)]
            if w[0]>w[1]:
                return 1
            elif w[0]<w[1]:
                return -1
        return 0

    def cmp_match(self, a, b):
        # 比较胜场数
        return -self.target_points[a]['match_win'] + self.target_points[b]['match_win']

    def cmp_game(self, a, b):
        # 比较净胜局数
        ga = self.target_points[a]['game_win'] - self.target_points[a]['game_lose']
        gb = self.target_points[b]['game_win'] - self.target_points[b]['game_lose']
        return gb-ga

    def cmp_score(self, a, b):
        # 比较净胜分
        sa = self.target_points[a]['score_win'] - self.target_points[a]['score_lose']
        sb = self.target_points[b]['score_win'] - self.target_points[b]['score_lose']
        return sb-sa

def give_rank(list, cmp, start=1):
    """
    >>> give_rank([1,2,2,2,3,4,4],operator.sub)
    [(1,1), (2,2), (2,2), (2,2), (5,3), (6,4), (7,4)]
    >>> give_rank([2,1,4,3,2,2,4],operator.sub)
    [(1,1), (2,2), (2,2), (2,2), (5,3), (6,4), (7,4)]
    """
    ls = sorted(list, cmp)
    li = gi = start
    rlist = [ (li, ls[0]) ]
    for i in range(1, len(ls)):
        li += 1
        if cmp(ls[i-1], ls[i]) == 0:
            rlist.append((gi, ls[i]))
        else:
            gi = li
            rlist.append((li, ls[i]))
    return rlist
