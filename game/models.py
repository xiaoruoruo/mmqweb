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

    name = CharField(max_length=50)
    text = TextField(blank=True)
    extra = TextField(default="{}") # json record
    participants= ManyToManyField('Participation', related_name='tournaments')

    def __unicode__(self):
        return u"%s" %(self.name)

    def textAsHtml(self):
        return re_linkURL.sub(replURL, self.text)

    def add_participant(self, player, represent, displayname=None):
        p = Participation()
        p.player = player
        p.represent = represent
        if displayname:
            p.displayname = displayname
        else:
            p.displayname = player.name
        p.save()
        self.participants.add(p)
        return p

    def get_participant(self, name=None, id=None):
        if id:
            p = self.participants.filter(player__id=id)
        elif name:
            p = self.participants.filter(displayname__exact=name)
        if p:
            return p[0]
        else:
            return None

class Participation(Model, Extension):
    displayname = CharField(max_length=50, blank=True)
    player = ForeignKey(Entity, related_name='player')
    represent = ForeignKey(Entity, related_name='represent', null=True, blank=True)

    def __unicode__(self):
        return self.displayname

    def save(self, *args, **kwargs):
        if not self.displayname:
            self.displayname = unicode(self.player)
        super(Participation, self).save(*args, **kwargs)

class Ranking(Model, Extension):
    RANKING_TYPES = (
            (1, "单淘汰"),
            (2, "单循环"),
            (3, "2n-1局n胜"),
            (4, "个人排名"),
            )
    type = IntegerField(choices=RANKING_TYPES)
    name = CharField(max_length=50, blank=True)
    matches = ManyToManyField('Match')

    """
    def get_ranking_targets(self):
        list=[]
        targets = self.xget("ranking_targets")
        if targets is None: return None
        # TODO in double game, there are id tuples
        for id in targets:
            list.append(Entity.objects.get(id=id))
        return list
    def set_ranking_targets(self, targets):
        ids = [t.id for t in targets]
        self.xset("ranking_targets",  ids)
    """
        
    def ranking(self):
        if self.type==2:
            # self.get_tournament().get_ranking_targets()
            #print("Match groups: %d" % self.matchgroup_set.count())
            if self.matchgroup_set.count() > 0:
                matches = self.matchgroup_set.all()[0].match_set.all()
            else:
                matches = self.matches.all()
            rank = ranker.RoundRobinRanker(None, matches)
            return rank.result()
        else:
            raise NotImplementedError
    
class MatchGroup(Model, Extension):
    """一些比赛Match的集合，有确定的ranking模式，以一种形式展现在网页上。
    """
    name = CharField(max_length=50)
    tournament = ForeignKey(Tournament)
    ranking = ForeignKey(Ranking, null=True, blank=True)
    view_name = CharField(max_length=50, blank=True)

    def addMatch(self, source):
        return parser.parseMatch(source, self)

    def __unicode__(self):
        return self.name

class Match(Model, Extension):
    """一场比赛，通常为三局两胜制。
    也可能是，两个团体之间的一次比赛，通常五个项目五局三胜，每一局是一个Match
    """

    match_group = ForeignKey(MatchGroup, null=True, blank=True)
    parent_match = ForeignKey('self', null=True, blank=True)
    result = IntegerField(null=True, blank=True) # 比赛结果，1,2代表赢家

    Team, Singles, Doubles = 1,2,3
    MATCH_TYPES= (
            (Team, "Team"),
            (Singles, "单打"),
            (Doubles, "双打"),
            )
    type = IntegerField(choices=MATCH_TYPES)

    player11 = ForeignKey(Entity, related_name="player11")
    player12 = ForeignKey(Entity, related_name="player12", null=True, blank=True)
    player21 = ForeignKey(Entity, related_name="player21")
    player22 = ForeignKey(Entity, related_name="player22", null=True, blank=True)

    text = TextField(blank=True)
    extra = TextField(default="{}") # json record

    def player1_str(self):
        # TODO should use Participation's displayname
        s = unicode(self.player11)
        if self.player12: s += u"/" + unicode(self.player12)
        return s
    def player2_str(self):
        s = unicode(self.player21)
        if self.player22: s += u"/" + unicode(self.player22)
        return s
    def title(self):
        p1, p2 = self.player1_str(), self.player2_str()
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

    def get_target(self, p, personal=False):
        """p=1 or 2
        personal: select the team it represents or select the player itself?
        """
        if p==1:
            p1,p2 = self.player11, self.player12
        else:
            p1,p2 = self.player21, self.player22

        pt = self.get_participant(p1)
        if pt and pt.represent and not personal:
            t = pt.represent
        else:
            if p2:
                t = (p1,p2)
            else:
                t = p1
        return t

    def get_participant(self, player):
        t = self.get_tournament()
        if not t: return None
        p = t.get_participant(id = player.id)
        if not p: return None
        return p

    def get_tournament(self):
        if self.match_group: return self.match_group.tournament
        if self.parent_match: return self.parent_match.get_tournament()
        return None

    def save(self, *args, **kwargs):
        if not self.type:
            if self.player12 or self.player22:
                self.type = Match.Doubles
            elif self.player11.type == Entity.Team or self.player21.type == Entity.Team:
                self.type = Match.Team
            else:
                self.type = Match.Singles
        super(Match, self).save(*args, **kwargs)

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
