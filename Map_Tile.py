from pico2d import *

import game_world

show_bb = False

# 지형 종류별 클래스
class Tile:
    image_grass = None
    image_dirt = None
    image_snow = None
    image_steel = None
    image_stone1 = None
    image_stone2 = None

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
            self.image_stone1 = load_image('tile_stone1.png')
            self.image_stone2 = load_image('tile_stone2.png')
            self.image_stone3 = load_image('tile_stone3.png')
            self.image_stone4 = load_image('tile_stone4.png')
            self.image_stone5 = load_image('tile_stone5.png')
            self.image_stonebrick = load_image('tile_stonebrick.png')

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
        elif self.type == 'tile_Stone1':
            self.image_stone1.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stone2':
            self.image_stone2.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stone3':
            self.image_stone3.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stone4':
            self.image_stone4.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stone5':
            self.image_stone5.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stonebrick':
            self.image_stonebrick.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)

# 충돌체크를 안해도되는 타일
class NonCollideTile:
    image_grass = None
    image_dirt = None
    image_snow = None
    image_steel = None
    image_stone1 = None
    image_stone2 = None

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
            self.image_stone1 = load_image('tile_stone1.png')
            self.image_stone2 = load_image('tile_stone2.png')
            self.image_stone3 = load_image('tile_stone3.png')
            self.image_stone4 = load_image('tile_stone4.png')
            self.image_stone5 = load_image('tile_stone5.png')
            self.image_stonebrick = load_image('tile_stonebrick.png')

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
        elif self.type == 'tile_Stone1':
            self.image_stone1.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stone2':
            self.image_stone2.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stone3':
            self.image_stone3.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stone4':
            self.image_stone4.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stone5':
            self.image_stone5.draw(self.x - self.scrollX, self.y)
        elif self.type == 'tile_Stonebrick':
            self.image_stonebrick.draw(self.x - self.scrollX, self.y)


# 객체 생성 함수
def makeTile(xPos, yPos, type, isCollide):
    if isCollide == 'Y':
        newTile = Tile()
    elif isCollide == 'N':
        newTile = NonCollideTile()

    newTile.x, newTile.y = xPos, yPos
    newTile.type = type

    game_world.add_object(newTile, 1)
