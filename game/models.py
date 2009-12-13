# encoding: utf-8
import json
from django.db.models import *
from namebook.models import Entity
import parser
import ranker

class Extension:
    def xget(self, key):
        return json.loads(self.extra).get(key)

    def xset(self, key, val):
        r = json.loads(self.extra)
        r[key] = val
        self.extra = json.dumps(r)

re_linkURL=re.compile(r'https?://([-\w\.]+)+(:\d+)?(/[-\w/_\.]*)?(\?\S+)?')
def replURL(m):
    # Replace picture URLs with img tag, replace bbs links with href tag
    url = m.group(0)
    ext = url[url.rfind('.')+1:]
    if ext in ['jpg','jpeg','png','bmp','svg']:
        return '<img src="%s">' % url
    elif url.startswith('http://bbs.sjtu.edu.cn/'):
        return '<a href="%s">%s</a>' % (url, url)
    else:
        return url

class Tournament(Model, Extension):
    "一次赛事，由许多场比赛Match组成"

    TOURNAMENT_TYPES= (
            (1, "单淘汰"),
            (2, "单循环"),
            )

    name = CharField(max_length=50)
    type = IntegerField(choices=TOURNAMENT_TYPES, null=True)
    participants = ManyToManyField(Entity, blank=True)
    text = TextField(blank=True)
    extra = TextField(default="{}") # json record

    def __unicode__(self):
        return u"%s" %(self.name)

    def textAsHtml(self):
        return re_linkURL.sub(replURL, self.text)

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

    def ranking(self):
        if self.match_set.count()==0: return []
        if self.type is None:
            raise ValueError("未指定比赛形式")
        if self.type==1:
            rank = ranker.RoundRobinRanker(self.get_ranking_targets(), self.match_set.all())
            return rank.result()
        else:
            raise NotImplementedError
    
    def get_ranking_targets(self):
        list=[]
        targets = self.xget("ranking_targets")
        if targets is None: return self.participants.all() #若未set过，返回所有participants
        for id in targets:
            list.append(Entity.objects.get(id=id))
        return list
    def set_ranking_targets(self, targets):
        ids = [t.id for t in targets]
        self.xset("ranking_targets",  ids)
        
class Match(Model, Extension):
    "一场比赛，通常为三局两胜制"

    tournament = ForeignKey(Tournament, null=True)
    result = IntegerField(null=True, blank=True) # 比赛结果，1,2代表赢家
    player1a = ForeignKey(Entity, related_name="player1a")
    player1b = ForeignKey(Entity, related_name="player1b", null=True, blank=True)
    player2a = ForeignKey(Entity, related_name="player2a")
    player2b = ForeignKey(Entity, related_name="player2b", null=True, blank=True)
    text = TextField(blank=True)
    extra = TextField(default="{}") # json record

    def title(self):
        p1, p2 = self.player1(), self.player2()
        if self.winner() == 1:
            p= p1 + u" 胜 " + p2
        elif self.winner() == 2:
            p= p1 + u" 负 " + p2
        else:
            p= p1 + u" 对 " + p2
        scores = " ".join([unicode(game) for game in self.game_set.all()])
        return p+" " + scores

    def __unicode__(self):
        return self.title() + "\n" + self.text
    
    def asHtml(self):
        return self.title() + "\n" + self.textAsHtml()

    def textAsHtml(self):
        return re_linkURL.sub(replURL, self.text)

    def player1(self):
        p1 = unicode(self.player1a.name)
        if self.player1b: p1 += u" " + unicode(self.player1b.name)
        return p1
    def player2(self):
        p2 = unicode(self.player2a.name)
        if self.player1b: p2 += u" " + unicode(self.player2b.name)
        return p2
        
    def winner(self):
        "set or guess the result"
        if not self.result:
            games=[0, 0, 0]
            for game in self.game_set.all():
                games[game.winner()] += 1
            if games[1] > games[2]:
                self.result = 1
            elif games[1] < games[2]:
                self.result = 2
            else:
                self.result = 0
        return self.result

class Game(Model, Extension):
    "一局比赛，通常为21分制"
    match = ForeignKey(Match)
    score1 = IntegerField()
    score2 = IntegerField()
    extra = TextField(default="{}") # json record

    def __unicode__(self):
        return u"%d:%d" % (self.score1, self.score2)

    def winner(self):
        if self.score1 > self.score2:
            return 1
        elif self.score1 < self.score2:
            return 2
        else:
            return 0
