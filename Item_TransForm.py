from pico2d import *

# 변신 아이템
class TransformItem():
    def __init__(self):  # 생성자
        self.image = load_image('item_fireflower.png')
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0

        self.itemValue = 0

        # 충돌 관련
        self.isCollipse = False

    def draw(self):
        if self.itemValue == 1:
            self.image = load_image('item_mushroom.png')
        elif self.itemValue == 2:
            self.image = load_image('item_fireflower.png')

        self.image.draw(self.x, self.y)



t_items = []
def make_titem(xPos, yPos, value):
    newtitem = TransformItem()
    newtitem.x, newtitem.y = xPos, yPos
    newtitem.itemValue = value
    t_items.append(newtitem)