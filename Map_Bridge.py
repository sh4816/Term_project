from pico2d import *

import game_world

show_bb = False

# 지형 종류별 클래스
class BridgeBoom:
    image = None
    image_boom = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None

        if self.image == None:
            self.image_boom = load_image('bridge_boom.png')

    def update(self):
        pass

    def draw(self):
        if self.type == 'bridge_Boom':
            self.image = self.image_boom

        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)

# 객체 생성 함수
def makeBridge(xPos, yPos, type):
    if type == 'bridge_Boom':
        newBridge = BridgeBoom()

    newBridge.x, newBridge.y = xPos, yPos
    newBridge.type = type

    game_world.add_object(newBridge, 1)
