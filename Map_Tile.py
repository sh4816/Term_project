from pico2d import *

# 지형
class Tile:
    def __init__(self):  # 생성자
        self.image = load_image('tile_grass.png')
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.type = "Grass"

    def draw(self):
        if self.type == "Grass":
            self.image = load_image('tile_grass.png')
        elif self.type == "SnowField":
            self.image = load_image('tile_snowfield.png')
        elif self.type == "Dirt":
            self.image = load_image('tile_dirt.png')

        self.image.draw(self.x, self.y)

tiles = []
def make_tile(xPos, yPos, type):
    newTile = Tile()
    newTile.x, newTile.y = xPos, yPos
    newTile.type = type

    tiles.append(newTile)

