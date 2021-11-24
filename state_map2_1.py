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

# state map
import state_map2_2


name = "Map2_1"

player = None

def enter():
    #=== 맵 배경
    bg = Map_Background.BG()
    bg.value = "map2_1"
    game_world.add_object(bg, 0)

    #=== 맵 오브젝트 불러오기
    MapEditor.editMap("map2_1")

    # Player 객체를 생성
    global player
    player = Player()
    # Game Data에서 Player 속성 읽어오기
    player.transform = game_data.gameData.transform
    if player.transform == P_Transform.T_Basic:
        player.frameX, player.frameY = 40, 30
        player.imageH = 300
    else:
        player.frameX, player.frameY = 40, 60
        player.y = 75
        player.imageH = 660

    game_world.add_object(player, 1)

    Trigger.makeTrigger(player.x, player.y, "autoMoving")


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
    # === 맵 이동 트리거
    global player
    for trigger in Trigger.triggers:
        if collideCheck(player, trigger) == 'right':
            if trigger.type == 'map_map2_2':
                print('Map 2-2 로 이동')  # test
                game_framework.change_state(state_map2_2)   # 맵 2-2 로 이동

    #=== Scroll Update
    for trigger in Trigger.triggers:
        trigger.scrollX = scrollMgr.getScrollX("Map2_1", player)

    for game_object in game_world.all_objects():
        game_object.scrollX = scrollMgr.getScrollX("Map2_1", player)
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for trigger in Trigger.triggers:
        trigger.draw()
    update_canvas()
