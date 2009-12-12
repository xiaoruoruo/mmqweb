# encoding: utf-8
from itertools import groupby

class Ranker:
    def __init__(self, targets, matches):
        """
        targets: target列表，每个target为一个Entity对象（单打，团体）或Entity tuple（双打）
        """
        raise NotImplementedError
    def result(self):
        "返回排好序的序列[(rank, target, comment), ...]"
        raise NotImplementedError
    
class RoundRobinRanker(Ranker):
    def find_target(self, a, b=None):
        "a,b: Entity"
        ca = set(a.categories.all()) # a所属的集合
        if b is None: ca.add(a) # 单打，则把他自己作为个人加入集合
        cs = ca.intersection(self.target_points.keys())
        if b:
            cb = set(c for c in b.categories.all() if c in self.target_points)
            cs = cs.intersection(cb) #计算a和b共同属于的集合
            if (a, b) in self.target_points: cs.add((a, b)) #加入双打双方作为一个积分对象
        if len(cs)>1:
            raise ValueError("玩家属于多个积分组")
        if len(cs)==0:
            raise ValueError("玩家不属于任何积分组")
        return cs.pop()
        
    def __init__(self, targets, matches):
        p = dict((target, {'match_win':0, 'game_win':0, 'game_lose':0,'score_win':0, 'score_lose':0}) for target in targets)
        self.target_points=p
        self.matches = {}
        for match in matches:
            t1 = self.find_target(match.player1a, match.player1b)
            t2 = self.find_target(match.player2a, match.player2b)
            self.matches[(t1, t2)] = match.winner()
            if match.winner()==1:
                p[t1]['match_win'] += 1
            elif match.winner()==2:
                p[t2]['match_win'] += 1
            
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
                        points = self.target_points[g1[1]]
                        result.append((rank1, g1[1], str_game))
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
                                result.append((rank2, g2[1], str_score))
                            elif len(g2)==2:
                                #如还剩2名（对）运动员净胜分数相等，则两者间比赛的胜者名次列前
                                a, b = give_rank([x[1] for x in g2], self.cmp_winner, rank2)
                                result.append((a[0], a[1], str_score))
                                result.append((b[0], b[1], str_score))
                            else:
                                #真的比不出来了
                                for g2i in g2:
                                    result.append((g2i[0], g2i[1], u"并列"))
            
        return result
    
    def cmp_winner(self, a, b):
        # a胜b返回-1，b胜a返回1
        if (a, b) in self.matches:
            w=self.matches[(a, b)]
            if w==1: 
                return -1
            elif w==2:
                return 1
        elif (b, a) in self.matches:
            w=self.matches[(b, a)]
            if w==1:
                return 1
            elif w==2:
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
