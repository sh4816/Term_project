# 오브젝트 스크롤
import Player

ScrollX = 0
MapLen = 0

def ScrollLock():
    if 0 <= Player.mario.x < 300:
        return True

    if Player.mario.x - ScrollX < 300:
        return True

    if ScrollX + 600 >= MapLen:
        return True

    return False


def getScroll_X(Map):

    if Map == "Map_1":
        MapLen = 2400

    if not ScrollLock():
        ScrollX = Player.mario.x - 300

    return ScrollX

