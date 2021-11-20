from pico2d import *

import game_world

show_bb = False

# 깃발 본체
class Flag:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 60, 450
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None

        self.image = load_image('flag.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)
# 받침 (Draw X)
class Prop:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None


        self.image = load_image('flag.png')

    def update(self):
        pass

    def draw(self):
        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)
# 기둥 (Draw X)
class Bar:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 10, 390
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None

        self.block_size = 30
        self.bar_width = 10

        self.image = load_image('flag.png')

    def update(self):
        pass

    def draw(self):
        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)


# 객체 생성 함수
def makeFlag(xPos, yPos):
    imgX, imgY = 30, 390

    newFlag = Flag()
    newFlag.x, newFlag.y = xPos, yPos

    game_world.add_object(newFlag, 1)

    newProp = Prop()
    newProp.x, newProp.y = xPos, yPos - imgY/2 + 15

    newBar = Bar()
    newBar.x, newBar.y = xPos, yPos + 30

    game_world.add_object(newProp, 1)
    game_world.add_object(newBar, 1)
