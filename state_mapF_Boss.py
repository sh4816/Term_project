from pico2d import *

import Trigger
import game_framework
import game_world
import ScrollManager as scrollMgr
import mob_kupa_breath
from collide import *

from player import Player, P_Transform
import game_data
import MapEditor
import Map_Background

import Map_Tile
import mob_kupa

#
import state_select

name = "MapF_Boss"

player = None

def enter():
    #=== 맵 배경
    bg = Map_Background.BG()
    bg.value = "mapF_Boss"
    game_world.add_object(bg, 0)

    #=== 맵 오브젝트 불러오기
    MapEditor.editMap("mapF_Boss")

    # Player 객체를 생성
    global player
    player = Player()
    # Game Data에서 Player 속성 읽어오기
    player.transform = game_data.gameData.transform
    if player.transform == P_Transform.T_Basic:
        player.frameX, player.frameY = 40, 30
        player.x, player.y = 75, 120
        player.imageH = 300
    else:
        player.frameX, player.frameY = 40, 60
        player.x, player.y = 75, 135
        player.imageH = 660

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
    if player.x >= 800 - player.frameX: player.x = 800 - player.frameX

    for obj in game_world.all_objects():
        # === 쿠파
        if obj.__class__ == mob_kupa.Kupa:
            if not obj.ismoving:
                # 착지하면 움직이기 시작한다.
                for tile in game_world.all_objects():
                    if tile.__class__ == Map_Tile.Tile:
                        if collideCheck(obj, tile) == 'bottom':
                            obj.ismoving = True
                            obj.state = mob_kupa.K_State.S_Idle
            else:
                if obj.x <= 0: obj.x = obj.frameX
                elif obj.x >= 800: obj.x = 800 - obj.frameX

                if not obj.state == mob_kupa.K_State.S_Hit:
                    if not obj.state == mob_kupa.K_State.S_Breath and not obj.state == mob_kupa.K_State.S_Hide:
                        # 쿠파는 플레이어가 있는 방향으로 움직인다.
                        if obj.dir == -1 and player.x - 100 > obj.x:
                            obj.dir = 1
                        elif obj.dir == 1 and player.x + 100 < obj.x:
                            obj.dir = -1

                        # 쿠파는 플레이어가 어느정도 멀어지면 대쉬로 빠르게 접근한다.
                        # if 180 < obj.dir * (player.x - obj.x) <= 250 and not obj.isFired:
                        #     obj.state = mob_kupa.K_State.S_Dash

                        # 쿠파는 플레이어가 완전 멀어진 상태에서 불덩이 발사가 쿨타임이 아닐 때 불덩이를 발사하는 공격을 한다.
                        if obj.dir * (player.x - obj.x) > 150 and not obj.breath_cooldown:
                            obj.state = mob_kupa.K_State.S_Breath

                        # 쿠파는 플레이어가 가까이에 있으면 걸어서 접근한다.
                        else:
                            if not obj.state == mob_kupa.K_State.S_Walk:
                                obj.state = mob_kupa.K_State.S_Walk


                    # 플레이어가 쿠파를 밟았을 때
                    if collideCheck(player, mob_kupa.kupa_bb) == 'bottom':
                        if obj.state == mob_kupa.K_State.S_Hide:
                            print('쿠파가 등딱지에 숨은 상태에서 밟으면 자신이 피해를 받는다')#test
                        else:       # 피격 무적 중일 때에는 밟아도 아무일 없음
                            if obj.life <= 0:
                                print('게임 클리어')#test
                            else:
                                obj.state = mob_kupa.K_State.S_Hit
                                obj.life -= 1
                                print(obj.state)
                    # 플레이어가 쿠파와 부딪혔을 때 (양 옆)
                    if not obj.state == mob_kupa.K_State.S_Hit:
                        if collideCheck(player, mob_kupa.kupa_bb) == 'left':
                            print('플레이어 데미지')#test
                        elif collideCheck(player, mob_kupa.kupa_bb) == 'right':
                            print('플레이어 데미지')#test

        # === 불꽃
        if obj.__class__ == mob_kupa_breath.KupaBreath:
            if obj.x < 0 or obj.x >= player.x + 800\
                    or obj.y < 0 or obj.y > 600:
                game_world.remove_object(obj)

            if not collideCheck(player, obj) == None:
                print('Hit by fire')#test

    # === 맵 이동 트리거
    for trigger in Trigger.triggers:
        if collideCheck(player, trigger) == 'left':
            if trigger.type == 'map_select':
                if player.stageclear and game_data.gameData.cur_stage <= game_data.gameData.unlocked_stage:
                    game_data.gameData.unlocked_stage += 1  # 다음 스테이지 해금
                    print('스테이지 ' + str(game_data.gameData.unlocked_stage) + ' 이 해금되었습니다.')  # test
                # Game Data 업데이트
                game_framework.change_state(state_select)  # 스테이지 선택화면으로 이동

    #=== Scroll Update
    for trigger in Trigger.triggers:
        trigger.scrollX = scrollMgr.getScrollX("MapF_Boss", player)

    for game_object in game_world.all_objects():
        game_object.scrollX = scrollMgr.getScrollX("MapF_Boss", player)
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for trigger in Trigger.triggers:
        trigger.draw()
    update_canvas()
