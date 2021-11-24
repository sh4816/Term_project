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
        player.frameX, player.frameY = 40, 30
        player.imageH = 300
    else:
        player.frameX, player.frameY = 40, 60
        player.imageH = 660

    player.y = 500

    game_world.add_object(player, 1)


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
    update_canvas()
