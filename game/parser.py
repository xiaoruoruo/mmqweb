# encoding: utf-8
import re
from django.db import transaction

import models

class ParseError(Exception):
    pass

pattern = re.compile(r"\s*(?P<p1a>\w+)(\s+(?P<p1b>\w+))?:\s*(?P<p2a>\w+)(\s+(?P<p2b>\w+))?\s+(?P<games>.+)", re.UNICODE) # 第一行语法
score_pattern = re.compile(r"(\d+):(\d+)") # 分数语法
@transaction.commit_on_success
def parseMatch(source, tournament):
    """
解析source中的文本，成功则创建相应的Match和Game，保存，返回Match。
source例子见tests.py
    """

    lines = source.replace(u"：",u":").split(u"\n",1)
    match = models.Match()
    match.tournament = tournament
    if len(lines) > 1: 
        # 注释评论
        match.comment = lines[1]
        # TODO 识别评论中的标注数据[attr:val]


    m = pattern.match(lines[0])
    if m:
        player_strs = [m.group("p1a"), m.group("p1b"), m.group("p2a"), m.group("p2b")]
        players = []
        for player_str in player_strs:
            if player_str is None: 
                players.append(None)
                continue
            player = tournament.get_or_add_participant(player_str)
            players.append(player)

        match.player1a, match.player1b, match.player2a, match.player2b = players
        match.save()

        n_game = 0
        n_p1win = 0
        # 识别局分
        games_str = m.group("games")
        if games_str:
            for gm in score_pattern.finditer(games_str):
                score1, score2 = int(gm.group(1)), int(gm.group(2))
                game = models.Game()
                game.score1, game.score2 = score1, score2
                game.match = match
                game.save()

                n_game += 1
                if score1 > score2: n_p1win += 1

        # 计算result
        if n_p1win > n_game/2:
            match.result = 1
        else:
            match.result = 2
        match.save()
    else:
        raise ParseError("格式错误")

    return match
