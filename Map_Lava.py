from pico2d import *

import game_framework
import game_world

show_bb = False

# 지형 종류별 클래스
class Lava:
    image = None
    image_T1 = None
    image_T2 = None
    image_T3 = None
    image_T4 = None
    image_B = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None
        self.slowAnimation = 1

        if self.image == None:
            self.image_T1 = load_image('lava_T1.png')
            self.image_T2 = load_image('lava_T2.png')
            self.image_T3 = load_image('lava_T3.png')
            self.image_T4 = load_image('lava_T4.png')
            self.image_B = load_image('lava_B.png')

    def update(self):
        if self.type < 5:
            self.slowAnimation += game_framework.frame_time * 5.0
            self.type = int(self.slowAnimation)
            if self.type >= 5:
                self.slowAnimation = 1
                self.type = 1
        pass

    def draw(self):
        if self.type == 1:
            self.image = self.image_T1
        elif self.type == 2:
            self.image = self.image_T2
        elif self.type == 3:
            self.image = self.image_T3
        elif self.type == 4:
            self.image = self.image_T4
        else:
            self.image = self.image_B

        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)

# 객체 생성 함수
def makeLava(xPos, yPos, type):
    newLava = Lava()

    newLava.x, newLava.y = xPos, yPos

    if type == "lava_T1":
        newLava.type = 1
        newLava.slowAnimation = 1
    elif type == "lava_T2":
        newLava.type = 2
        newLava.slowAnimation = 2
    elif type == "lava_T3":
        newLava.type = 3
        newLava.slowAnimation = 3
    elif type == "lava_T4":
        newLava.type = 4
        newLava.slowAnimation = 4
    else:
        newLava.type = 9

    game_world.add_object(newLava, 1)
