from pico2d import *

import game_framework
import game_world

show_bb = False

# 벽돌
class Brick():
    image = None
    image1 = None
    image2 = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.imgType = None

        # 충돌 관련
        self.nonDestroyCollide = False
        self.nonDestroyMoving = 0

        # 이미지
        if self.image == None:
            self.image = load_image('block_brick.png')
            self.image1 = load_image('block_brick.png')
            self.image2 = load_image('block_brick2.png')

    def update(self):
        if self.nonDestroyCollide:
            if self.nonDestroyMoving < 8.0:
                print(self.nonDestroyMoving)
                self.nonDestroyMoving += game_framework.frame_time * 100
            else:
                self.nonDestroyMoving = 0
                self.nonDestroyCollide = False


    def draw(self):
        if self.imgType == "Default":
            self.image = self.image1
        elif self.imgType == "Blue":
            self.image = self.image2

        self.image.draw(self.x - self.scrollX, self.y + self.nonDestroyMoving)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)



# 벽돌
def makeBrick(xPos, yPos, image_type):
    newBrick = Brick()
    newBrick.x, newBrick.y = xPos, yPos
    newBrick.imgType = image_type

    game_world.add_object(newBrick, 1)
