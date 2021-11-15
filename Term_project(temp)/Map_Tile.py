from pico2d import *

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


# 객체 생성 함수
tiles = []
def makeTile(xPos, yPos, type):
    # newGrass = TileGrass()
    # newGrass.x, newTile.y = xPos, yPos
    # newGrass.type = type
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

    tiles.append(newTile)
