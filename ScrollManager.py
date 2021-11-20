# 오브젝트 스크롤
import player

ScrollX = 0
MapLen = 0

def ScrollLock(player):
    global ScrollX, MapLen

    if 0 <= player.x < 300:
        return "Lock_LeftEnd"
    elif player.x - ScrollX < 300:
        return "Lock_LeftMoving"
    elif ScrollX + 600 >= MapLen:
        return "Lock_RightEnd"

    return "NonLock"


def getScrollX(Map, player):
    global ScrollX, MapLen

    if Map == "Map1":
        MapLen = 6600
    elif Map == "Map2_1":
        MapLen = 600
    elif Map == "Map2_2":
        MapLen = 4650

    if ScrollLock(player) == "NonLock":
        ScrollX = player.x - 300
    elif ScrollLock(player) == "Lock_LeftEnd":
        ScrollX = 0
    elif ScrollLock(player) == "Lock_LeftMoving":
        ScrollX = player.scrollX
    elif ScrollLock(player) == "Lock_RightEnd":
        ScrollX = MapLen - 600

    return ScrollX

