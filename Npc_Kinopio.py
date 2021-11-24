from pico2d import *
import enum

import Map_Bridge
import game_framework
import game_world
from collide import collideCheck
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe

show_bb = False

class K_State(enum.IntEnum):
    S_Idle = 0
    S_Hello = enum.auto()

class Kinopio():
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 60  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.state = K_State.S_Idle

        # 이미지
        if self.image == None:
            self.image = load_image('kinopio.png')

    def update(self):
        pass

    def draw(self):
        # 렌더링
        self.image.clip_draw(int(self.state) * self.frameX, 0, self.frameX, self.frameY
                             , self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)


def makeKino(xPos, yPos):
    newNPC = Kinopio()
    newNPC.x, newNPC.y = xPos, yPos - 15

    game_world.add_object(newNPC, 1)
