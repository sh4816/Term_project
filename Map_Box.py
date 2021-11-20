from pico2d import *
import enum

import game_world

show_bb = False

class boxType(enum.IntEnum):
    coin = 0
    mushroom = enum.auto()
    flower = enum.auto()

# 물음표 박스
class Box_Question():
    image = None
    image_used = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.frame = 0
        self.slowFrame = 0
        self.itemValue = 0                 # 충돌하면 튀어나오는 아이템 종류 (1: 코인, 2: 버섯, 3: 파이어플라워)

        # 충돌 관련
        self.isCollipse = False
        self.isUsed = False
        self.CollipseDir = 0 # 1: 위 2: 아래

        # 이미지
        if self.image == None:
            self.image = load_image('block_question.png')
            self.image_used = load_image('block_used.png')


    def update(self):
        pass

    def draw(self):
        if self.isUsed:
            self.image_used.draw(self.x - self.scrollX, self.y)
        else:
            self.slowFrame += 1
            self.frame = (self.slowFrame // 10) % 4
            self.image.clip_draw(self.frame * self.frameX, 0, self.frameX, self.frameY, self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)


def makeBox(xPos, yPos, box_type):
    newBox = Box_Question()
    newBox.x, newBox.y = xPos, yPos
    if box_type == "box_Coin":
        newBox.itemValue = boxType.coin
    elif box_type == "box_Mushroom":
        newBox.itemValue = boxType.mushroom
    elif box_type == "box_Flower":
        newBox.itemValue = boxType.flower

    game_world.add_object(newBox, 1)
