from pico2d import *

import game_world

import Obstacle_Rotatedfire

show_bb = False

class RotatedfireCenter:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None

        if self.image == None:
            self.image = load_image('block_used.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)


# 객체 생성 함수
def makeCenter(xPos, yPos):
    newCenter = RotatedfireCenter()

    newCenter.x, newCenter.y = xPos, yPos

    game_world.add_object(newCenter, 1)

    for i in range(1, 10+1):
        Obstacle_Rotatedfire.makeFires(newCenter.x, newCenter.y, 10*i)

