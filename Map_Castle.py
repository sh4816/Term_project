from pico2d import *

show_bb = False

class Castle:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 210, 90
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None

        self.image = load_image('castle.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)
            draw_rectangle(self.x - 15 - self.scrollX, self.y - self.frameY / 2 + 30
                           , self.x + 15 - self.scrollX, self.y - self.frameY / 2)


# 객체 생성 함수
castles = []
def makeCastle(xPos, yPos):
    newCastle = Castle()
    newCastle.x, newCastle.y = xPos, yPos
    castles.append(newCastle)

