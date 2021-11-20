from pico2d import *
import game_world

# 동전
class Coin():
    def __init__(self):  # 생성자
        self.image = load_image('coin.png')
        self.frameX, self.frameY = 20, 20  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.frame = 0
        self.slowFrame = 0
        self.x, self.y = 0, 0
        self.scrollX = 0

        self.isEffect = False

        # 충돌 관련
        self.isCollipse = False
        self.isUsed = False

    def update(self):
        pass

    def draw(self):
        self.slowFrame += 1
        self.frame = (self.slowFrame // 10) % 4
        self.image.clip_draw(self.frame * self.frameX, 0, self.frameX, self.frameY, self.x - self.scrollX, self.y)

        if self.isEffect:
            if self.slowFrame >= 40:
                game_world.remove_object(self)


# 코인 생성 (맵에 배치될 코인)
def make_coins(xPos, yPos, effect):
    newcoin = Coin()
    newcoin.x, newcoin.y = xPos, yPos
    if effect:
        newcoin.isEffect = True
    else:
        newcoin.isUsed = True

    game_world.add_object(newcoin, 1)
