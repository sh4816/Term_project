from pico2d import *

# 벽돌
class Brick():
    def __init__(self):  # 생성자
        self.image = load_image('block_brick.png')
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0

        # 충돌 관련
        self.isCollipse = False
        self.destroy = 0

    def update(self):
        pass#
        # # 충돌체크
        # # 1. 충돌하면 1을 더한다.
        # if collipseCheck(mario.frameX, mario.frameY, mario.x, mario.y + 1,
        #                  self.frameX, self.frameY, self.x, self.y, True):
        #     if mario.status == c_state.S_Jump and mario.y < self.y:  # 마리오가 블록 아래에서 점프 중
        #         self.destroy += 1
        #         self.isCollipse += 1
        #     elif mario.status == c_state.S_GP and mario.y > self.y:  # 마리오가 그라운드 파운드로 위에서 아래로 찍음
        #         self.destroy += 1
        #         self.isCollipse += 1
        # # 2. 하나라도 충돌했다면 0이 아니게 됨
        # if not self.isCollipse == 0:
        #     if not self.destroy == 0:
        #         bricks.remove(self)

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)



# 벽돌
bricks = []
def makeBrick(xPos, yPos):
    newBrick = Brick()
    newBrick.x, newBrick.y = xPos, yPos
    bricks.append(newBrick)