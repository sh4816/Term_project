import game_framework
from pico2d import *
import game_world
from collide import collideCheck

PIXEL_PER_METER = (10.0 / 0.3) #10 pixel 30cm boy.py와 동일
SHOOT_SPEED_KMPH = 100.0
SHOOT_SPEED_MPM = (SHOOT_SPEED_KMPH * 1000.0 / 60.0)
SHOOT_SPEED_MPS = (SHOOT_SPEED_MPM / 60.0)
SHOOT_SPEED_PPS = (SHOOT_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Fireball:
    image = None

    def __init__(self):
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.frameX, self.frameY = 20, 20
        self.frame = 0
        self.velocity = SHOOT_SPEED_PPS

        # 이동
        self.dir = -1

        if Fireball.image == None:
            Fireball.image = load_image('fireball.png')

    def draw(self):
        self.image.clip_draw(int(self.frame) * self.frameX, 0, self.frameX, self.frameY, self.x - self.scrollX, self.y)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        self.x += self.velocity * game_framework.frame_time

        # 충돌 체크

        # 맵을 벗어나면 삭제
        if self.x < 0 or self.x > 8000:
            game_world.remove_object(self)

fireballs = []

def removeAll():
    print('파이어볼 전체 삭제')
    for obj in fireballs:
        fireballs.remove(obj)