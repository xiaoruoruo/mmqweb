# encoding: utf-8
import re

import models

class ParseError(Exception):
    pass

pattern = re.compile(ur"\s*(?P<p1a>\w+)([\s、，,/]+(?P<p1b>\w+))?\s*(:|vs|胜|负|对)\s*(?P<p2a>\w+)([\s、，,/]+(?P<p2b>\w+))?(?P<games>\s+.+)", re.UNICODE | re.IGNORECASE) # 第一行语法
# 分数语法
scores_pattern = re.compile(r"([\s,]+-?\d+:-?\d+)+$")
score_pattern = re.compile(r"(-?\d+):(-?\d+)")
sdata_pattern = re.compile(ur"\[(\w+):([^]]+)\]", re.UNICODE) # 标注数据

def updateText(match, text):
    # 注释评论
    match.text = text
    # 识别评论中的标注数据[attr:val]
    for m in sdata_pattern.finditer(text):
        match.xset(m.group(1), m.group(2))

def parseMatch(source, match_group):
    """
解析source中的文本，成功则创建相应的Match和Game，保存，返回Match。
source例子见tests.py
    """

    lines = source.replace(u"：",u":").split(u"\n",1)
    match = models.Match()
    if match_group:
        match.match_group = match_group
        tournament = match_group.tournament
    else:
        tournament = None
    if len(lines) > 1:
        updateText(match, lines[1])

    m = pattern.match(lines[0])
    if m:
        player_strs = [m.group("p1a"), m.group("p1b"), m.group("p2a"), m.group("p2b")]
        players = []
        for player_str in player_strs:
            if player_str:
                name = player_str
                player = tournament.get_participant(name)
                if not player:
                    raise ParseError(u"未报名选手：%s" % name)
                players.append(player.player)
            else:
                players.append(None)

        match.player11, match.player12, match.player21, match.player22 = players
        match.save()

        # 识别局分
        games_str = m.group("games")
        if not scores_pattern.match(games_str):
            raise ParseError(u"分数部分格式错误:%s" % games_str)
        for gm in score_pattern.finditer(games_str):
            score1, score2 = int(gm.group(1)), int(gm.group(2))
            game = models.Game()
            game.score1, game.score2 = score1, score2
            game.match = match
            game.save()
    else:
        raise ParseError(u"格式错误:%s" % lines[0])

    return match
