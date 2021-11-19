from pico2d import *

show_bb = False

class Flag:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 60, 450
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None

        self.block_size = 60
        self.bar_width = 10

        self.image = load_image('flag.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            # 받침
            draw_rectangle(self.x - self.block_size/2 - self.scrollX, self.y - self.frameY + self.block_size
                           , self.x + self.block_size/2 - self.scrollX, self.y - self.frameY)
            # 깃대
            draw_rectangle(self.x - self.bar_width/2 - self.scrollX, self.y + self.frameY
                           , self.x + self.bar_width/2 - self.scrollX, self.y - self.frameY + self.block_size)


# 객체 생성 함수
flags = []
def makeFlag(xPos, yPos):
    newFlag = Flag()
    newFlag.x, newFlag.y = xPos, yPos
    flags.append(newFlag)


def removeAll():
    print('깃발 전체 삭제')
    for obj in flags:
        flags.remove(obj)
