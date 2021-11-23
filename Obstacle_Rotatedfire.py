from pico2d import *

import math
import game_world
import game_framework

show_bb = False

# 지형 종류별 클래스
class RotatedFire:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 10, 10  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.cx, self.cy = 0, 0
        self.x, self.y = 0, 0
        self.timer = 0
        self.radius = 0
        self.degree = 0
        self.scrollX = 0

        if self.image == None:
            self.image = load_image('rotated_fire.png')

    def update(self):
        self.timer += game_framework.frame_time * 100.0
        self.degree = self.timer % 360

        self.x = self.cx + self.radius * math.cos(math.radians(self.degree))
        self.y = self.cy + self.radius * math.sin(math.radians(self.degree))
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)


# 객체 생성 함수
def makeFires(cx, cy, radius):
    newFire = RotatedFire()
    newFire.cx, newFire.cy = cx, cy
    newFire.radius = radius

    game_world.add_object(newFire, 1)
