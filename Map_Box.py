from pico2d import *

# 물음표 박스
class Box_Question():
    def __init__(self):  # 생성자
        self.image = load_image('block_question.png')
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.frame = 0
        self.slowFrame = 0
        self.itemValue = 0                 # 충돌하면 튀어나오는 아이템 종류 (0: 코인, 1: 버섯, 2: 파이어플라워)

        # 충돌 관련
        self.isCollipse = False
        self.isUsed = False
        self.CollipseDir = 0 # 1: 위 2: 아래

    def update(self):
        if self.isUsed: self.image = load_image('block_used.png')
        else:           self.image = load_image('block_question.png')

    def draw(self):
        if self.isUsed:
            self.image.draw(self.x, self.y)
            #self.image.clip_draw(self.frame * self.frameX, 0, self.frameX, self.frameY, self.x, self.y)
        else:
            self.slowFrame += 1
            self.frame = (self.slowFrame // 5) % 4
            self.image.clip_draw(self.frame * self.frameX, 0, self.frameX, self.frameY, self.x, self.y)


boxes = []
def make_box(xPos, yPos, box_type):
    newBox = Box_Question()
    newBox.x, newBox.y = xPos, yPos
    newBox.itemValue = box_type
    boxes.append(newBox)