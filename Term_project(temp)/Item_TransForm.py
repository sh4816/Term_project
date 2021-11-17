from pico2d import *
from collide import collideCheck
from enum import *
import Map_Tile
import Map_Box
import Map_Brick

class Value(IntEnum):
    Mushroom = 0
    Fireflower = auto()

show_bb = False

# 변신 아이템
class TransformItem():
    def __init__(self):  # 생성자
        self.image = load_image('item_fireflower.png')
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0

        self.itemValue = 0

        # 충돌 관련
        self.isOnGround = 0
        self.landYPos = 0

    def update(self):
        if self.itemValue == Value.Mushroom:
            # 1. 충돌하면 1을 더한다.
            for tile in Map_Tile.tiles:
                if collideCheck(self, tile):
                    self.isOnGround += 1
                    self.y = tile.y + tile.frameY/2 + self.frameY/2
            for box in Map_Box.boxes:
                if collideCheck(self, box):
                    self.isOnGround += 1
                    self.y = box.y + box.frameY / 2 + self.frameY / 2
            for brick in Map_Brick.bricks:
                if collideCheck(self, brick):
                    self.isOnGround += 1
                    self.y = brick.y + brick.frameY / 2 + self.frameY / 2
            # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
            if self.isOnGround == 0:
                self.y -= 4
            else:
                self.x += 2
                self.isOnGround = 0

            if self.y < 0:
                transItems.remove(self)
                print('removed')#

    def draw(self):
        # 이미지 선택
        if self.itemValue == Value.Mushroom:
            if not self.image == 'item_mushroom.png':
                self.image = load_image('item_mushroom.png')
        elif self.itemValue == Value.Fireflower:
            if not self.image == 'item_fireflower.png':
                self.image = load_image('item_fireflower.png')

        # 렌더링
        self.image.draw(self.x - self.scrollX, self.y)

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