from pico2d import *

import Trigger
import game_world

show_bb = False

# 배관
class Pipe:
    image = None

    image_LT, image_MT, image_RT = None, None, None
    image_LM, image_MM, image_RM = None, None, None
    image_LB, image_MB, image_RB = None, None, None
    imageL_LT, imageL_MT, imageL_RT = None, None, None
    imageL_LM, imageL_MM, imageL_RM = None, None, None
    imageL_LB, imageL_MB, imageL_RB = None, None, None

    def __init__(self):  # 생성자
        global image_LT, image_MT, image_RT,image_LM, image_MM, image_RM, image_LB, image_MB, image_RB
        global imageL_LT, imageL_MT, imageL_RT, imageL_LM, imageL_MM, imageL_RM, imageL_LB, imageL_MB, imageL_RB

        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = ""

        # Image Load
        if self.image == None:
            self.image = load_image('pipe_greenLT.png')
            self.image_LT = load_image('pipe_greenLT.png')
            self.image_MT = load_image('pipe_greenMT.png')
            self.image_RT = load_image('pipe_greenRT.png')
            self.image_LM = load_image('pipe_greenLM.png')
            self.image_MM = load_image('pipe_greenMM.png')
            self.image_RM = load_image('pipe_greenRM.png')
            self.image_LB = load_image('pipe_greenLB.png')
            self.image_MB = load_image('pipe_greenMB.png')
            self.image_RB = load_image('pipe_greenRB.png')
            self.imageL_LT = load_image('pipeL_greenLT.png')
            self.imageL_MT = load_image('pipeL_greenMT.png')
            self.imageL_RT = load_image('pipeL_greenRT.png')
            self.imageL_LM = load_image('pipeL_greenLM.png')
            self.imageL_MM = load_image('pipeL_greenMM.png')
            self.imageL_RM = load_image('pipeL_greenRM.png')
            self.imageL_LB = load_image('pipeL_greenLB.png')
            self.imageL_MB = load_image('pipeL_greenMB.png')
            self.imageL_RB = load_image('pipeL_greenRB.png')

        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        if self.type == "pipe_greenLT":
            self.image = self.image_LT
        elif self.type == "pipe_greenMT":
            self.image = self.image_MT
        elif self.type == "pipe_greenRT":
            self.image = self.image_RT
        elif self.type == "pipe_greenLM":
            self.image = self.image_LM
        elif self.type == "pipe_greenMM":
            self.image = self.image_MM
        elif self.type == "pipe_greenRM":
            self.image = self.image_RM
        elif self.type == "pipe_greenLB":
            self.image = self.image_LB
        elif self.type == "pipe_greenMB":
            self.image = self.image_MB
        elif self.type == "pipe_greenRB":
            self.image = self.image_RB
        #Left
        elif self.type == "pipeL_greenLT":
            self.image = self.imageL_LT
        elif self.type == "pipeL_greenMT":
            self.image = self.imageL_MT
        elif self.type == "pipeL_greenRT":
            self.image = self.imageL_RT
        elif self.type == "pipeL_greenLM":
            self.image = self.imageL_LM
        elif self.type == "pipeL_greenMM":
            self.image = self.imageL_MM
        elif self.type == "pipeL_greenRM":
            self.image = self.imageL_RM
        elif self.type == "pipeL_greenLB":
            self.image = self.imageL_LB
        elif self.type == "pipeL_greenMB":
            self.image = self.imageL_MB
        elif self.type == "pipeL_greenRB":
            self.image = self.imageL_RB

        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)

            if self.type == "pipeL_greenLB" or self.type == "pipeL_greenLM" or self.type == "pipeL_greenLT":
                draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                               , self.x - self.scrollX, self.y - self.frameY / 2)
                self.font.draw(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2 + 10, 'Trigger',
                               (0, 0, 255))

def makePipe(xPos, yPos, type):
    newPipe = Pipe()
    newPipe.x, newPipe.y = xPos, yPos
    newPipe.type = type
    # if newPipe.type == "pipeL_greenLB" or newPipe.type == "pipeL_greenLM" or newPipe.type == "pipeL_greenLT":
    #     Trigger.makeTrigger(newPipe.x, newPipe.y, 'map_select')

    game_world.add_object(newPipe, 1)

