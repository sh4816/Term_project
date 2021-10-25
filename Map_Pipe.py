from pico2d import *

# 배관
class Pipe:
    def __init__(self):  # 생성자
        self.image = load_image('pipe_greenLT.png')
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = ""

    def update(self):
        pass

    def draw(self):
        if self.type == "pipe_greenLT":
            self.image = load_image('pipe_greenLT.png')
        elif self.type == "pipe_greenMT":
            self.image = load_image('pipe_greenMT.png')
        elif self.type == "pipe_greenRT":
            self.image = load_image('pipe_greenRT.png')
        elif self.type == "pipe_greenLM":
            self.image = load_image('pipe_greenLM.png')
        elif self.type == "pipe_greenMM":
            self.image = load_image('pipe_greenMM.png')
        elif self.type == "pipe_greenRM":
            self.image = load_image('pipe_greenRM.png')
        elif self.type == "pipe_greenLB":
            self.image = load_image('pipe_greenLB.png')
        elif self.type == "pipe_greenMB":
            self.image = load_image('pipe_greenMB.png')
        elif self.type == "pipe_greenRB":
            self.image = load_image('pipe_greenRB.png')

        self.image.draw(self.x - self.scrollX, self.y)

pipes = []
def makePipe(xPos, yPos, type):
    newPipe = Pipe()
    newPipe.x, newPipe.y = xPos, yPos
    newPipe.type = type

    pipes.append(newPipe)

