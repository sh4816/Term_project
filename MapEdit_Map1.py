import Map_Background
import Map_Tile
import Map_Box
import Map_Brick

tileSize = 30

# 배경
def mapEdit():
    Map_Background.make_bg("Map1")


    # 타일
    for i in range(100):
        Map_Tile.make_tile(i*tileSize, 60, "Grass")

    # for i in range(30):
    #     Map_Tile.make_tile(i*tileSize, 0, "Dirt")
    #     Map_Tile.make_tile(i*tileSize, 30, "Dirt")


    # 그 외의 오브젝트

    Map_Box.make_box(25*tileSize, 180, "Coin")

    Map_Brick.make_brick(29*tileSize, 180)
    Map_Box.make_box(30*tileSize, 180, "Mushroom")
    Map_Brick.make_brick(31*tileSize, 180)
    Map_Box.make_box(32*tileSize, 180, "Coin")
    Map_Brick.make_brick(33*tileSize, 180)

    Map_Box.make_box(31*tileSize, 300, "Coin")

