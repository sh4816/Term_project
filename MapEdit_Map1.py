import Map_Background
import Map_Tile
import Map_Box
import Map_Brick

tileSize = 30

# 배경
def mapEdit():
    Map_Background.make_bg("Map1")


    # 타일
    for i in range(30):
        Map_Tile.make_tile(i*tileSize, 60, "Grass")

    for i in range(30):
        Map_Tile.make_tile(i*tileSize, 0, "Dirt")
        Map_Tile.make_tile(i*tileSize, 30, "Dirt")


    # 그 외의 오브젝트

    Map_Box.make_box(5*tileSize, 180, "Coin")

    Map_Brick.make_brick(9*tileSize, 180)
    Map_Box.make_box(10*tileSize, 180, "Mushroom")
    Map_Brick.make_brick(11*tileSize, 180)
    Map_Box.make_box(12*tileSize, 180, "Coin")
    Map_Brick.make_brick(13*tileSize, 180)

    Map_Box.make_box(11*tileSize, 300, "Coin")

