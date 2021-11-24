import enum

from pico2d import *

import math
import game_world
import game_framework

show_bb = False

PIXEL_PER_METER = (30.0 / 1.0)  # 30 pixel == 1m

# Moving Speed
def KMPH2MPS(KMPH): # km/h -> m/sec
    MPM = KMPH * 1000.0 / 60.0
    MPS = MPM / 60.0
    return MPS      #return m/sec

MOVE_SPEED_PPS = (KMPH2MPS(50) * PIXEL_PER_METER)

class F_Direction(enum.IntEnum):
    D_Up = 0
    D_Mid = enum.auto()
    D_Down = enum.auto()
    D_Sin = enum.auto()

class KupaBreath:
    image = None
    imageL = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.startY = self.y
        self.frame = 0
        self.scrollX = 0
        self.dir = -1
        self.up_mid_down = None

        self.distance = 0

        if self.image == None:
            self.image = load_image('kupa_fire.png')
            self.imageL = load_image('kupa_fireL.png')

    def update(self):
        self.frame += game_framework.frame_time
        movingLen = self.dir * MOVE_SPEED_PPS * game_framework.frame_time
        self.x += movingLen
        self.distance += movingLen

        if self.dir == 1:
            if self.up_mid_down == int(F_Direction.D_Up):
                self.y += (1/3) * movingLen
            elif self.up_mid_down == int(F_Direction.D_Down):
                self.y -= (1/3) * movingLen
            elif self.up_mid_down == int(F_Direction.D_Sin):
                self.y = math.sin(math.radians(self.distance)) * 60 + self.startY
        else:
            if self.up_mid_down == int(F_Direction.D_Up):
                self.y -= (1/3) * movingLen
            elif self.up_mid_down == int(F_Direction.D_Down):
                self.y += (1/3) * movingLen
            elif self.up_mid_down == int(F_Direction.D_Sin):
                self.y = math.sin(math.radians(self.distance)) * 60 + self.startY

    def draw(self):
        # 렌더링
        randerY = 0
        if self.up_mid_down == 3:
            randerY = 1
        elif self.up_mid_down == 4:
            randerY = 1
        else:
            randerY = self.up_mid_down
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) % 3 * self.frameX, 60 - randerY * self.frameY
                                 , self.frameX, self.frameY, self.x - self.scrollX, self.y)
        else:
            self.imageL.clip_draw(int(self.frame) % 3 * self.frameX, 60 - randerY * self.frameY
                                  , self.frameX, self.frameY, self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)


# 객체 생성 함수
def makeFires(xPos, yPos, dir, UMD):
    newFire = KupaBreath()
    newFire.x, newFire.y = xPos, yPos
    newFire.startY = newFire.y
    newFire.dir = dir
    newFire.up_mid_down = UMD

    game_world.add_object(newFire, 1)
