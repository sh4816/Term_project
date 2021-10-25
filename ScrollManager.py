# 오브젝트 스크롤
import Player

ScrollX = 0
MapLen = 0

def ScrollLock(player):
    global ScrollX, MapLen

    if 0 <= player.x < 300:
        return True
    elif player.x - ScrollX < 300:
        return True
    elif ScrollX + 600 >= MapLen:
        return True

    return False


def getScrollX(Map, player):
    global ScrollX, MapLen


    if Map == "Map1":
        MapLen = 6600

    if not ScrollLock(player):
        ScrollX = player.x - 300

    return ScrollX

