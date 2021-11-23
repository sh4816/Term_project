from pico2d import *

import game_world
import game_framework

show_bb = False

# Physics Variables...
#
PIXEL_PER_METER = (30.0 / 1.0)  # 30 pixel == 1m
# Moving Speed
def KMPH2MPS(KMPH): # km/h -> m/sec
    MPM = KMPH * 1000.0 / 60.0
    MPS = MPM / 60.0
    return MPS      #return m/sec

MOVE_SPEED_PPS = (KMPH2MPS(5) * PIXEL_PER_METER)

class MovingTile:
    image = None
    image_pipe_SL = None
    image_pipe_SM = None
    image_pipe_SR = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None

        self.isMoving = False
        self.ver_or_hor = None
        self.dir = 1
        self.distance = 0           # 움직인 거리
        self.max_distance = 0       # 움직일 수 있는 최대 거리
        self.velocity = self.dir * MOVE_SPEED_PPS

        if self.image == None:
            self.image = load_image('pipeL_steelL.png')
            self.image_pipe_SL = load_image('pipeL_steelL.png')
            self.image_pipe_SM = load_image('pipeL_steelM.png')
            self.image_pipe_SR = load_image('pipeL_steelR.png')

    def update(self):
        if self.ver_or_hor == 'vertical':
            self.y += self.dir * self.velocity * game_framework.frame_time
        elif self.ver_or_hor == 'horizontal':
            self.x += self.dir * self.velocity * game_framework.frame_time

        self.distance += self.dir * self.velocity * game_framework.frame_time
        # 일정 거리를 왔다갔다하면서 반복 운동한다
        if self.distance <= 0:
            self.dir = (-1) * self.dir  # 방향바꾸기
            self.distance = 0
        elif self.distance >= self.max_distance:
            self.dir = (-1) * self.dir  # 방향바꾸기
            self.distance = self.max_distance

    def draw(self):
        if self.type == 'pipeL_steelL':
            self.image = self.image_pipe_SL
        elif self.type == 'pipeL_steelM':
            self.image = self.image_pipe_SM
        elif self.type == 'pipeL_steelR':
            self.image = self.image_pipe_SR

        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)



# 객체 생성 함수
def makeMovingTile(xPos, yPos, type, vh, max_dis, dir):
    newMovingTile = MovingTile()

    newMovingTile.x, newMovingTile.y = xPos, yPos
    newMovingTile.type = type

    newMovingTile.ver_or_hor = vh
    newMovingTile.max_distance = max_dis
    newMovingTile.dir = dir
    if newMovingTile.dir == 1:
        newMovingTile.distance = 0
    else:
        newMovingTile.distance = newMovingTile.max_distance

    game_world.add_object(newMovingTile, 1)
