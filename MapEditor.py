from enum import *

import Item_Coin
import Map_Background
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe
import Map_Castle
import Map_Flag
import Map_MovingTile
import Map_Bridge
import Map_Lava
import Npc_Kinopio
import Obstacle_Rotatedfire_Center
import Obstacle_Button
import mob_goomba
import Trigger
import mob_kupa
import Npc_Kinopio

ground_data_file = None
obj_data_file = None
mob_data_file = None

def editMap(mapName):
    global ground_data_file, obj_data_file, mob_data_file
    #=== initialize
    size = 30

    # 읽어올 파일 이름
    if mapName == "map1":
        ground_file_name = "Data_Map_1_ground.txt"
        obj_file_name = "Data_Map_1_obj.txt"
        mob_file_name = "Data_Map_1_mob.txt"
    elif mapName == "map2_1":
        ground_file_name = "Data_Map_2_1_ground.txt"
        obj_file_name = "Data_Map_2_1_obj.txt"
        mob_file_name = "Data_Map_2_1_mob.txt"
    elif mapName == "map2_2":
        ground_file_name = "Data_Map_2_2_ground.txt"
        obj_file_name = "Data_Map_2_2_obj.txt"
        mob_file_name = "Data_Map_2_2_mob.txt"
    elif mapName == "map2_3":
        ground_file_name = "Data_Map_2_3_ground.txt"
        obj_file_name = "Data_Map_2_3_obj.txt"
        mob_file_name = None
    elif mapName == "map3":
        ground_file_name = "Data_Map_3_ground.txt"
        obj_file_name = "Data_Map_3_obj.txt"
        mob_file_name = "Data_Map_3_mob.txt"
    elif mapName == "mapF_Boss":
        ground_file_name = "Data_Map_F_Boss_ground.txt"
        obj_file_name = "Data_Map_F_Boss_obj.txt"
        mob_file_name = "Data_Map_F_Boss_mob.txt"


    #=== 지형 Ground
    ground_repeat = 0
    ground_xPos, ground_yPos = 0, 0
    ground_type = ""
    ground_isCollide = ""
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
            ground_isCollide = data_map_ground[4]

            for i in range(ground_repeat):
                Map_Tile.makeTile((ground_xPos + i)*size, ground_yPos*size, ground_type, ground_isCollide)

        except:
            break
    ground_data_file.close()


    #=== 오브젝트 Obj
    # 지형 obj
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
                Map_Tile.makeTile(obj_xPos*size, obj_yPos*size, obj_name, 'Y')
            elif obj_type == "box":
                Map_Box.makeBox(obj_xPos*size, obj_yPos*size, obj_name)
            elif obj_type == "brick":
                Map_Brick.makeBrick(obj_xPos*size, obj_yPos*size, obj_name)
            elif obj_type == "pipe":
                Map_Pipe.makePipe(obj_xPos*size, obj_yPos*size, obj_name)
            elif obj_type == "pipeT_Map2Map": # pipe trigger - 맵 state 이동
                Map_Pipe.makePipe(obj_xPos*size, obj_yPos*size, obj_name)
                if mapName == "map2_1":
                    Trigger.makeTrigger(obj_xPos*size, obj_yPos*size, 'map_map2_2')
                elif mapName == "map2_2":
                    Trigger.makeTrigger(obj_xPos*size, obj_yPos*size, 'map_map2_3')
            elif obj_type == "pipeT_transPos": # pipe trigger - 좌표 변환
                Map_Pipe.makePipe(obj_xPos*size, obj_yPos*size, obj_name)
                if mapName == "map2_2":
                    Trigger.makeTrigger(obj_xPos*size, obj_yPos*size, 'trans2_2')
            elif obj_type == "moving_VU":
                maxdis = 0
                if mapName == "map2_2":
                    maxdis = 400
                Map_MovingTile.makeMovingTile(obj_xPos*size, obj_yPos*size, obj_name, 'vertical', maxdis, 1)
            elif obj_type == "moving_VD":
                maxdis = 0
                if mapName == "map2_2":
                    maxdis = 400
                Map_MovingTile.makeMovingTile(obj_xPos*size, obj_yPos*size, obj_name, 'vertical', maxdis, -1)
            elif obj_type == "moving_HR":
                maxdis = 0
                if mapName == "map3":
                    maxdis = 60
                Map_MovingTile.makeMovingTile(obj_xPos * size, obj_yPos * size, obj_name, 'horizontal', maxdis, 1)
            elif obj_type == "moving_HL":
                maxdis = 0
                if mapName == "map3":
                    maxdis = 60
                Map_MovingTile.makeMovingTile(obj_xPos * size, obj_yPos * size, obj_name, 'horizontal', maxdis, -1)
            elif obj_type == "bridge":
                Map_Bridge.makeBridge(obj_xPos * size, obj_yPos * size, obj_name)
            elif obj_type == "lava":
                Map_Lava.makeLava(obj_xPos * size, obj_yPos * size, obj_name)
            elif obj_type == "obstacle":
                if obj_name == "obs_RFC":
                    Obstacle_Rotatedfire_Center.makeCenter(obj_xPos * size, obj_yPos * size)
                elif obj_name == "obs_Button":
                    Obstacle_Button.makeButton(obj_xPos * size, obj_yPos * size)
            elif obj_type == "coin":
                Item_Coin.make_coins(obj_xPos*size, obj_yPos*size, False)
            elif obj_type == "castle":
                Map_Castle.makeCastle(obj_xPos*size, obj_yPos*size)
            elif obj_type == "flag":
                Map_Flag.makeFlag(obj_xPos*size, obj_yPos*size)
            elif obj_type == "npc":
                if obj_name == "npc_Kinopio":
                    Npc_Kinopio.makeKino(obj_xPos*size, obj_yPos*size)

        except:
            break
    obj_data_file.close()

    # 몹 obj
    if not mob_file_name == None:
        mob_xPos, mob_yPos = 0, 0
        mob_type = ""
        mob_name = ""
        mob_dir = 1

        data_map_mob = []

        mob_data_file = open(mob_file_name, "r", encoding="utf8")

        while True:
            try:
                data_mob_line = mob_data_file.readline()

                data_mob_obj = data_mob_line.split()

                mob_xPos = float(data_mob_obj[0])
                mob_yPos = float(data_mob_obj[1])
                mob_type = data_mob_obj[2]
                mob_dir = int(data_mob_obj[3])

                if mob_type == "goomba":
                    mob_goomba.makeGoombas(mob_xPos*size, mob_yPos*size, mob_dir)
                elif mob_type == "kupa":
                    print('start making kupa...')
                    mob_kupa.makeKupa(mob_xPos*size, mob_yPos*size, mob_dir)
                    print('kupa is made in ' + str((mob_xPos*size, mob_yPos*size)))

            except:
                break
        mob_data_file.close()
