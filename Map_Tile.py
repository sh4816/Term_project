from pico2d import *

import game_world

show_bb = False

# 지형 종류별 클래스
class TileGrass:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = "tile_Grass"

        if self.image == None:
            self.image = load_image('tile_grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)


class TileDirt:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = "tile_Dirt"

        if self.image == None:
            self.image = load_image('tile_dirt.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)

class TileSteel:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = "tile_Steel"

        if self.image == None:
            self.image = load_image('block_steel.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)

class TileSnowfield:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = "tile_Snowfield"

        if self.image == None:
            self.image = load_image('tile_snowfield.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)


# 객체 생성 함수
tiles = []
def makeTile(xPos, yPos, type):
    if type == "tile_Grass":
        newTile = TileGrass()
    elif type == "tile_Dirt":
        newTile = TileDirt()
    elif type == "tile_Steel":
        newTile = TileSteel()
    elif type == "tile_Snowfiled":
        newTile = TileSnowfield()

    newTile.x, newTile.y = xPos, yPos
    newTile.type = type

    game_world.add_object(newTile, 1)
    #tiles.append(newTile)

def removeAll():
    print('타일 전체 삭제')
    for obj in tiles:
        tiles.remove(obj)

