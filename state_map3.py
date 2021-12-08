from pico2d import *

import Map_Bridge
import Npc_Kinopio
import Obstacle_Button
import ScrollManager
import Trigger
import game_framework
import game_world
import ScrollManager as scrollMgr
from collide import *

from player import Player, P_Transform
import game_data
import MapEditor
import Map_Background

import Map_Lava
import mob_kupa
import Obstacle_Rotatedfire
import Obstacle_Button

#
import state_select

name = "Map3"

player = None

image_status = None
image_numstat = None

playtime = 300

def enter():
    #=== 맵 배경
    bg = Map_Background.BG()
    bg.value = "map3"
    game_world.add_object(bg, 0)

    #=== 맵 오브젝트 불러오기
    MapEditor.editMap("map3")

    # Player 객체를 생성
    global player
    player = Player()
    # Game Data에서 Player 속성 읽어오기
    player.transform = game_data.gameData.transform
    if player.transform == P_Transform.T_Basic:
        player.frameX, player.frameY = 30, 30
        player.x, player.y = 75, 360
        player.imageH = 300
    else:
        player.frameX, player.frameY = 30, 60
        player.x, player.y = 75, 375
        player.imageH = 600

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
    global player, name
    #=== 회전하는불꽃, 용암, 버튼
    for obj in game_world.all_objects():
        if obj.__class__ == Map_Lava.Lava:
            if obj.type < 5:
                if not collideCheck(player, obj) == None:
                    print('Game over - Lava')#
        if obj.__class__ == Obstacle_Rotatedfire.RotatedFire:
            if not collideCheck(player, obj) == None:
                print('Hit by Fire')#
        if obj.__class__ == Obstacle_Button.BoomButton:
            if collideCheck(player, obj) == 'bottom':
                for target in game_world.all_objects():
                    if target.__class__ == Map_Bridge.BridgeBoom:
                        game_world.remove_object(target)

        if obj.__class__ == Npc_Kinopio.Kinopio:
            if player.x + 150 >= obj.x:
                obj.state = Npc_Kinopio.K_State.S_Hello
            else:
                obj.state = Npc_Kinopio.K_State.S_Idle

            if not collideCheck(player, obj) == None:
                print('우리 공주 여기없음')
                if player.stageclear and game_data.gameData.cur_stage <= game_data.gameData.unlocked_stage:
                    game_data.gameData.unlocked_stage += 1  # 다음 스테이지 해금
                    print('스테이지 ' + str(game_data.gameData.unlocked_stage) + ' 이 해금되었습니다.')  # test
                # Game Data 업데이트
                game_framework.change_state(state_select)  # 스테이지 선택화면으로 이동

    #=== 쿠파
    for kupa in game_world.all_objects():
        if kupa.__class__ == mob_kupa.Kupa:
            if not kupa.ismoving:
                if player.x + 600 >= kupa.x:    # 쿠파는 화면에 들어왔을 때부터 움직이기 시작한다.
                    kupa.ismoving = True
                    kupa.state = mob_kupa.K_State.S_Walk
            else:
                # 쿠파는 플레이어가 있는 방향으로 움직인다.
                if kupa.dir == -1 and player.x - 100 > kupa.x: kupa.dir = 1
                elif kupa.dir == 1 and player.x + 100 < kupa.x: kupa.dir = -1

                # 쿠파는 플레이어가 멀어지면 대쉬로 빠르게 접근한다.
                if kupa.dir * (player.x - kupa.x) > 200: kupa.state = mob_kupa.K_State.S_Dash
                else: kupa.state = mob_kupa.K_State.S_Walk

            if kupa.y <= 150:
                name = "Map3_ending" # 맵스크롤 할 수 있는 길이를 늘려 Scroll lock을 해제한다.
                game_world.remove_object(kupa)

    # === 맵 이동 트리거
    for trigger in Trigger.triggers:
        if collideCheck(player, trigger) == 'left':
            if trigger.type == 'map_select':
                if player.stageclear and game_data.gameData.cur_stage <= game_data.gameData.unlocked_stage:
                    game_data.gameData.unlocked_stage += 1  # 다음 스테이지 해금
                    print('스테이지 ' + str(game_data.gameData.unlocked_stage) + ' 이 해금되었습니다.')  # test
                # Game Data 업데이트
                game_framework.change_state(state_select)  # 스테이지 선택화면으로 이동

    # === 플레이어 사망 (스테이지 선택화면으로 다시 이동.)
    if player.transform <= -1:
        game_data.gameData.life -= 1
        if game_data.gameData.life > 0:
            game_framework.change_state(state_select)  # 스테이지 선택화면으로 이동
        else:
            print('게임오버 화면 추가해서 그쪽으로 이동시킬 예정.')  # temp

    #=== Scroll
    for trigger in Trigger.triggers:
        trigger.scrollX = scrollMgr.getScrollX(name, player)

    for game_object in game_world.all_objects():
        game_object.scrollX = scrollMgr.getScrollX(name, player)
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
