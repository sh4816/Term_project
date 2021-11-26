import enum

class P_Transform(enum.IntEnum):
    T_Basic = 0
    T_Super = enum.auto()
    T_Fire = enum.auto()

class GameData:
    def __init__(self):
        # 맵 선택
        self.cur_stage = 1
        self.unlocked_stage = 1
        # 점수
        self.score = 0
        self.coin = 0
        # 마리오
        self.life = 5
        self.transform = P_Transform.T_Basic

gameData = GameData()