from pico2d import *
import game_framework
import game_world
from collide import collideCheck
import enum
import player
import game_data
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe

# Physics Variables...
#
# 마리오의 키는 2M, 몸무게는 70kg 이라 가정,
PIXEL_PER_METER = (30.0 / 1.0)  # 30 pixel == 1m

# Player Run Speed
def KMPH2MPS(KMPH): # km/h -> m/sec
    MPM = KMPH * 1000.0 / 60.0
    MPS = MPM / 60.0
    return MPS      #return m/sec

MOVE_SPEED_PPS = (KMPH2MPS(10) * PIXEL_PER_METER)
GRAVITY_ACCEL_PPS2 = -400.0 # px/s^2

# enum
class Value(enum.IntEnum):
    Mushroom = 0
    Fireflower = enum.auto()

show_bb = False

# 변신 아이템
class TransformItem():
    image_mush = None
    image_flower = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0

        self.dir = 1
        self.timerFall = 0

        self.itemValue = 0

        # 충돌 관련
        self.isOnGround = 0
        self.landYPos = 0

        # 이미지
        if self.image_mush == None:
            self.image_mush = load_image('item_mushroom.png')
            self.image_flower = load_image('item_fireflower.png')

    def update(self):
        #=== 플레이어와 충돌하면 플레이어의 변신상태 변경
        # 충돌 체크
        # collipse = False
        # if collideCheck(self, player) == None:
        #     collipse = True
        #
        # # 충돌하면 캐릭터 상태변경
        # if collipse:
        #     if self.itemValue == Value.Mushroom:
        #         if game_data.gameData.transform < player.P_Transform.T_Super:
        #             game_data.gameData.transform = player.P_Transform.T_Super
        #     elif self.itemValue == Value.Fireflower:
        #         if game_data.gameData.transform < player.P_Transform.T_Fire:
        #             game_data.gameData.transform = player.P_Transform.T_Fire
        #
        #     # transItems.remove(self)
        #     # game_world.remove_object(self)

        if self.itemValue == Value.Mushroom:
            #=== 왼쪽 오른쪽으로 이동
            # 충돌 체크 (왼쪽 or 오른쪽이이 오브젝트로 혀있는지 확인)
            collipse = False
            checkCount = 0
            while (not collipse and checkCount < 4):
                if checkCount == 0:
                    for box in Map_Box.boxes:
                        if collideCheck(self, box) == "left" or collideCheck(self, box) == "right":
                            collipse = True
                            break
                elif checkCount == 1:
                    for brick in Map_Brick.bricks:
                        if collideCheck(self, brick) == "left" or collideCheck(self, brick) == "right":
                            collipse = True
                            break
                elif checkCount == 2:
                    for pipe in Map_Pipe.pipes:
                        if collideCheck(self, pipe) == "left" or collideCheck(self, pipe) == "right":
                            collipse = True
                            break
                elif checkCount == 3:
                    for tile in Map_Tile.tiles:
                        if collideCheck(self, tile) == "left" or collideCheck(self, tile) == "right":
                            collipse = True
                            break

                checkCount += 1
            # 충돌하지 않았을 때에만 이동
            if collipse:
                self.dir = (-1) * self.dir  # 방향전환
                self.x += self.dir * MOVE_SPEED_PPS * game_framework.frame_time
            else:
                self.x += self.dir * MOVE_SPEED_PPS * game_framework.frame_time
                self.x = clamp(25, self.x, 6600 - 25)


            #=== 바닥에 아무것도 없으면(허공에 있으면) 아래로 낙하
            collipse = False
            checkCount = 0
            while (not collipse and checkCount < 4):
                if checkCount == 0:
                    for box in Map_Box.boxes:
                        if collideCheck(self, box) == "bottom":
                            self.y = box.y + box.frameY
                            collipse = True
                            break
                elif checkCount == 1:
                    for brick in Map_Brick.bricks:
                        if collideCheck(self, brick) == "bottom":
                            self.y = brick.y + brick.frameY
                            collipse = True
                            break
                elif checkCount == 2:
                    for pipe in Map_Pipe.pipes:
                        if collideCheck(self, pipe) == "bottom":
                            self.y = pipe.y + pipe.frameY
                            collipse = True
                            break
                elif checkCount == 3:
                    for tile in Map_Tile.tiles:
                        if collideCheck(self, tile) == "bottom":
                            self.y = tile.y + tile.frameY
                            collipse = True
                            break

                checkCount += 1

            if not collipse:
                self.timerFall += game_framework.frame_time
                self.y += GRAVITY_ACCEL_PPS2 * (self.timerFall ** 2) # v = v0 + gt, d = v * t
            else:
                if not self.timerFall == 0:
                    self.timerFall = 0

            if self.y < 0 or self.x < 0:
                transItems.remove(self)
                print('removed')#

    def draw(self):
        # 렌더링
        if self.itemValue == Value.Mushroom:
            self.image_mush.draw(self.x - self.scrollX, self.y)
        elif self.itemValue == Value.Fireflower:
            self.image_flower.draw(self.x - self.scrollX, self.y)

        # self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)



transItems = []
def make_transItem(xPos, yPos, value):
    newitem = TransformItem()
    newitem.x, newitem.y = xPos, yPos
    newitem.itemValue = value
    transItems.append(newitem)