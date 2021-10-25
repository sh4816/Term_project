from enum import *
import Map_Background
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe


def editMap(mapName):
    #=== initialize
    size = 30

    # 읽어올 파일 이름
    if mapName == "map1":
        ground_file_name = "Data_Map_1_ground.txt"
        obj_file_name = "Data_Map_1_obj.txt"


    # 지형 Ground
    ground_repeat = 0
    ground_xPos, ground_yPos = 0, 0
    ground_type = ""
    data_map_ground = []

    ground_data_file = open(ground_file_name, "r", encoding="utf8")

    while True:
        try:
            data_ground_line = ground_data_file.readline()
            data_map_ground = data_ground_line.split()

            ground_repeat = int(data_map_ground[0])
            ground_xPos = float(data_map_ground[1])
            ground_yPos = float(data_map_ground[2])
            ground_type = data_map_ground[3]

            for i in range(ground_repeat):
                Map_Tile.makeTile((ground_xPos + i)*size, ground_yPos*size, ground_type)

        except:
            break


    # 오브젝트 Obj
    obj_xPos, obj_yPos = 0, 0
    obj_type = ""
    obj_name = ""
    data_map_obj = []

    obj_data_file = open(obj_file_name, "r", encoding="utf8")

    while True:
        try:
            data_obj_line = obj_data_file.readline()

            data_map_obj = data_obj_line.split()

            obj_xPos = float(data_map_obj[0])
            obj_yPos = float(data_map_obj[1])
            obj_type = data_map_obj[2]
            obj_name = data_map_obj[3]

            if obj_type == "tile":
                Map_Tile.makeTile(obj_xPos*size, obj_yPos*size, obj_name)
            elif obj_type == "box":
                Map_Box.makeBox(obj_xPos*size, obj_yPos*size, obj_name)
            elif obj_type == "brick":
                Map_Brick.makeBrick(obj_xPos*size, obj_yPos*size)
            elif obj_type == "pipe":
                Map_Pipe.makePipe(obj_xPos*size, obj_yPos*size, obj_name)

        except:
            break


    obj_data_file.close()
