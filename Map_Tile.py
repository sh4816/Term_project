from pico2d import *

import game_world

show_bb = False

# 지형 종류별 클래스
class Tile:
    image_grass = None
    image_dirt = None
    image_snow = None
    image_steel = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None

        if self.image_grass == None:
            self.image_grass = load_image('tile_grass.png')
            self.image_dirt = load_image('tile_dirt.png')
            self.image_snow = load_image('tile_snowfield.png')
            self.image_steel = load_image('tile_steel.png')

    def update(self):
        pass

    def draw(self):
        if self.type == 'tile_Grass':
            self.image_grass.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Dirt':
            self.image_dirt.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Snow':
            self.image_snow.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Steel':
            self.image_steel.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)



# 객체 생성 함수
def makeTile(xPos, yPos, type):
    newTile = Tile()

    newTile.x, newTile.y = xPos, yPos
    newTile.type = type

    game_world.add_object(newTile, 1)
