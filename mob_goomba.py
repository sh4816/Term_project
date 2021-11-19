from pico2d import *
import enum
import game_framework
import game_world
from collide import collideCheck
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe

# Physics Variables...
#
# 마리오의 키는 2M, 몸무게는 70kg 이라 가정,
PIXEL_PER_METER = (30.0 / 1.0)  # 30 pixel == 1m

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

# Player Run Speed
def KMPH2MPS(KMPH): # km/h -> m/sec
    MPM = KMPH * 1000.0 / 60.0
    MPS = MPM / 60.0
    return MPS      #return m/sec

MOVE_SPEED_PPS = (KMPH2MPS(5) * PIXEL_PER_METER)
DASH_SPPED_PPS = (KMPH2MPS(15) * PIXEL_PER_METER)
GRAVITY_ACCEL_PPS2 = -400.0 # px/s^2


# enum
class G_State(enum.IntEnum):
    Walk = 0
    Dead_by_turtle = enum.auto()
    Dash = enum.auto()
    Dead = enum.auto()


show_bb = False

class Goomba():
    image = None
    imageL = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.frame = 0
        self.state = G_State.Walk

        self.ismoving = False   # 굼바는 화면에 처음으로 잡혔을 때부터 움직이기 시작한다.

        self.dir = 1
        self.timerFall = 0

        self.itemValue = 0
        self.isReverse = False  # 거꾸로 되어있는지

        # 충돌 관련
        self.isOnGround = 0
        self.landYPos = 0

        # 이미지
        if self.image == None:
            self.image = load_image('goomba.png')
            self.imageL = load_image('goombaL.png')

    def update(self):
        if self.ismoving:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

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

            # 움직임
            if self.state == G_State.Walk:
                self.x += self.dir * MOVE_SPEED_PPS * game_framework.frame_time
            elif self.state == G_State.Dash:
                self.x += self.dir * DASH_SPPED_PPS * game_framework.frame_time


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
                goombas.remove(self)
                game_world.remove_object(self)

    def draw(self):
        # 렌더링
        if not self.state == G_State.Dead:
            if self.dir == 1:
                self.image.clip_draw(int(self.frame)*self.frameX, 60 - int(self.state) * self.frameY, self.frameX, self.frameY
                                     , self.x - self.scrollX, self.y)
            else:
                self.imageL.clip_draw(int(self.frame) * self.frameX, 60 - int(self.state) * self.frameY, self.frameX, self.frameY
                                     , self.x - self.scrollX, self.y)
        else:
            self.image.clip_draw(int(self.frame)*self.frameX, 0, self.frameX, self.frameY/10
                                     , self.x - self.scrollX, self.y)

        # self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)



goombas = []
def makeGoombas(xPos, yPos, dir):
    newmob = Goomba()
    newmob.x, newmob.y = xPos, yPos
    newmob.dir = dir
    goombas.append(newmob)


def removeAll():
    print('굼바 전체 삭제')
    for obj in goombas:
        goombas.remove(obj)
