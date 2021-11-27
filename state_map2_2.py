from pico2d import *

import Trigger
import game_framework
import game_world
import ScrollManager as scrollMgr
from collide import *

from player import Player, P_Transform
import game_data
import MapEditor
import Map_Background
import mob_goomba

#
import state_map2_3


name = "Map2_2"

player = None

image_status = None
image_numstat = None

playtime = 300

def enter():
    #=== 맵 배경
    bg = Map_Background.BG()
    bg.value = "map2_2"
    game_world.add_object(bg, 0)

    #=== 맵 오브젝트 불러오기
    MapEditor.editMap("map2_2")

    # Player 객체를 생성
    global player
    player = Player()
    # Game Data에서 Player 속성 읽어오기
    player.transform = game_data.gameData.transform
    if player.transform == P_Transform.T_Basic:
        player.frameX, player.frameY = 30, 30
        player.imageH = 300
    else:
        player.frameX, player.frameY = 30, 60
        player.imageH = 600

    player.y = 500

    game_world.add_object(player, 1)


    global image_status, image_numstat
    if image_status == None:
        image_status = load_image('img_status.png')
        image_numstat = load_image('numbers_status.png')


def exit():
    Trigger.remove_all_triggers()
    for game_object in game_world.all_objects():
        game_world.remove_object(game_object)
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            player.handle_event(event)


def update():
    global player
    # === 캐릭터가 일정범위 접근해 있어야 오브젝트들이 움직인다.
    for obj in game_world.all_objects():
        if obj.__class__ == mob_goomba.Goomba:
            if player.x + 600 >= obj.x:
                obj.isMoving = True

    # === 맵 이동 트리거
    for trigger in Trigger.triggers:
        if collideCheck(player, trigger) == 'bottom':
            if trigger.type == 'trans2_2':
                player.collide_trigger = True
                break
        if collideCheck(player, trigger) == 'right':
            if trigger.type == 'map_map2_3':
                print('Map 2-3 로 이동')  # test
                game_framework.change_state(state_map2_3)  # 맵 2-3 로 이동
                break
        else:
            player.collide_trigger = False

    #=== Scroll Update
    for trigger in Trigger.triggers:
        trigger.scrollX = scrollMgr.getScrollX("Map2_2", player)

    for game_object in game_world.all_objects():
        game_object.scrollX = scrollMgr.getScrollX("Map2_2", player)
        game_object.update()


def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()
    for trigger in Trigger.triggers:
        trigger.draw()

        # === 상태창 (score, coin, stage, time)
        global image_status, image_numstat
        image_status.draw(400, 540)
        # score
        drawNumbers('score', 0)
        # coin
        drawNumbers('coin', 1)
        # stage
        drawNumbers('stage', 0)
        # time
        drawNumbers('time', 0)

    update_canvas()

def drawNumbers(type, color):
    global image_status, image_numstat, playtime

    fullnum = 0
    if type == 'score':
        fullnum = game_data.gameData.score
    elif type == 'coin':
        fullnum = game_data.gameData.coin
    elif type == 'stage':
        fullnum = game_data.gameData.cur_stage
    elif type == 'time':
        playtime -= game_framework.frame_time
        fullnum = int(playtime)

    if type == 'score' and game_data.gameData.score == 0:
        image_numstat.clip_draw(0, 20 * color, 20, 20, 105, 535)
    elif type == 'coin' and game_data.gameData.coin == 0:
        image_numstat.clip_draw(0, 20 * color, 20, 20, 305, 535)
    elif type == 'stage' and game_data.gameData.cur_stage == 0:
        image_numstat.clip_draw(0, 20 * color, 20, 20, 455, 535)
    elif type == 'time' and playtime == 0:
        image_numstat.clip_draw(0, 20 * color, 20, 20, 665, 535)
    else:
        # 1. 몇 자리 숫자인지 구하기
        cur_score = fullnum
        positional_num = 0
        while cur_score >= 1:
            positional_num += 1
            cur_score /= 10
        # 2. 각 자릿수 구하기
        cur_score = fullnum
        for i in range(positional_num):
            digit = cur_score % 10

            cur_score /= 10
            #print(cur_score, ', ', i, '번째 숫자: ', int(digit)) # test

            if type == 'score':
                image_numstat.clip_draw(int(digit) * 20, 20 * color, 20, 20, 65 + 11 * (positional_num-i), 535)
            elif type == 'coin':
                image_numstat.clip_draw(int(digit) * 20, 20 * color, 20, 20, 305 + 11 * (positional_num-i), 535)
            elif type == 'stage':
                image_numstat.clip_draw(int(digit) * 20, 20 * color, 20, 20, 455 + 11 * (positional_num-i), 535)
            elif type == 'time':
                image_numstat.clip_draw(int(digit) * 20, 20 * color, 20, 20, 665 + 11 * (positional_num-i), 535)
