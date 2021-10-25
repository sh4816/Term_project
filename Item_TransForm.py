from pico2d import *
from Collide import collipseCheck
from enum import *
import Map_Tile
import Map_Box
import Map_Brick

class Value(IntEnum):
    NN = auto()#
    Mushroom = auto()
    Fireflower = auto()

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
                if collipseCheck(self.frameX - 2, self.frameY, self.x, self.y,
                                 tile.frameX, tile.frameY, tile.x, tile.y, False):
                    self.isOnGround += 1
                    self.y = tile.y + tile.frameY/2 + self.frameY/2
            for box in Map_Box.boxes:
                if collipseCheck(self.frameX - 2, self.frameY, self.x, self.y,
                                 box.frameX, box.frameY, box.x, box.y, False):
                    self.isOnGround += 1
                    self.y = box.y + box.frameY / 2 + self.frameY / 2
            for brick in Map_Brick.bricks:
                if collipseCheck(self.frameX - 2, self.frameY, self.x, self.y,
                                 brick.frameX, brick.frameY, brick.x, brick.y, False):
                    self.isOnGround += 1
                    self.y = brick.y + brick.frameY / 2 + self.frameY / 2
            # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
            if self.isOnGround == 0:
                self.y -= 4
            else:
                self.x += 2
                self.isOnGround = 0

            if self.y < 0:
                t_items.remove(self)
                print('removed')

    def draw(self):
        if self.itemValue == Value.Mushroom:
            self.image = load_image('item_mushroom.png')
        elif self.itemValue == Value.Fireflower:
            self.image = load_image('item_fireflower.png')

        self.image.draw(self.x - self.scrollX, self.y)



t_items = []
def make_titem(xPos, yPos, value):
    newtitem = TransformItem()
    newtitem.x, newtitem.y = xPos, yPos
    newtitem.itemValue = value
    t_items.append(newtitem)