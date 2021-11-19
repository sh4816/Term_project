from pico2d import *

show_bb = False

# 벽돌
class Brick():
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0

        # 충돌 관련
        self.isCollipse = False
        self.destroy = 0

        # 이미지
        if self.image == None:
            self.image = load_image('block_brick.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)



# 벽돌
bricks = []
def makeBrick(xPos, yPos):
    newBrick = Brick()
    newBrick.x, newBrick.y = xPos, yPos
    bricks.append(newBrick)


def removeAll():
    print('벽돌 전체 삭제')
    for obj in bricks:
        bricks.remove(obj)