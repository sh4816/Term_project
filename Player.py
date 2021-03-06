import mob_kupa_breath

import Npc_Kinopio

import Map_Bridge
import Map_Lava
import Map_MovingTile
import Obstacle_Button
import Obstacle_Rotatedfire
import Obstacle_Rotatedfire_Center
import game_framework
import mob_kupa
import mob_kupa_breath


import state_select
# import state_map2_2
#import state_map2_2

import mob_goomba
from collide import *
from pico2d import *

import Trigger

import game_data
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe
import Map_Castle
import Map_Flag
import Map_MovingTile
import Map_Bridge
import Item_Coin
import Item_TransForm
import ball

import game_world
import enum

# Physics Variables...
#
# 마리오의 키는 2M, 몸무게는 70kg 이라 가정,
PIXEL_PER_METER = (30.0 / 1.0)  # 30 pixel == 1m

# Player Run Speed
def KMPH2MPS(KMPH): # km/h -> m/sec
    MPM = KMPH * 1000.0 / 60.0
    MPS = MPM / 60.0
    return MPS      #return m/sec

RUN_SPEED_KMPH = 10.0           # km/h
RUN_SPEED_PPS = (KMPH2MPS(RUN_SPEED_KMPH) * PIXEL_PER_METER)

DASH_SPEED_KMPH = 30.0          # km/h
DASH_SPEED_PPS = (KMPH2MPS(DASH_SPEED_KMPH) * PIXEL_PER_METER)

SHOOT_SPEED_KMPH = 100.0        # km/h
SHOOT_SPEED_PPS = (KMPH2MPS(SHOOT_SPEED_KMPH) * PIXEL_PER_METER)

# Player Jump Speed
JUMP_V0_PPS = 330.0 # px/s
GRAVITY_ACCEL_PPS2 = -400.0 # px/s^2


# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

# State
# 변신 상태
class P_Transform(enum.IntEnum):
    T_Basic = 0
    T_Super = enum.auto()
    T_Fire = enum.auto()

# 동작 상태
class P_State(enum.IntEnum):
    S_Idle = 1
    S_Run = enum.auto()
    S_Dash = enum.auto()
    S_Jump = enum.auto()
    S_Down = enum.auto()
    S_GP = enum.auto()
    S_Climb = enum.auto()
    S_Hit = enum.auto()
    S_Action = enum.auto()
    S_Die_Transform = enum.auto()


# Player Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP\
    ,UP_DOWN, DOWN_DOWN, UP_UP, DOWN_UP\
    ,SHIFT_DOWN, SHIFT_UP\
    ,SPACE\
    ,FALLING_EVENT, LANDING_EVENT, LANDING_RUN_EVENT, LANDING_DASH_EVENT\
    ,TRANSLATE_EVENT, TRANS2IDLE_EVENT, TRANS2RUN_EVENT, TRANS2DASH_EVENT, TRANS2JUMP\
    ,HIT_EVENT, HIT2IDLE_EVENT, HIT2RUN_EVENT, HIT2DASH_EVENT, HIT2JUMP_EVENT\
    ,STAGECLEAR_EVENT = range(26)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,

    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,

    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,

    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


# Player States

class IdleState:

    def enter(player, event):
        player.velocity = 0
        player.frame = 0  # IdleState는 애니메이션이 없음.
        # player.timer = 1000 # 오랫동안 입력이 없을 때

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

        if player.isDoubleInput:
            player.isDoubleInput = False
            if event == LEFT_UP:
                player.add_event(RIGHT_DOWN)
            elif event == RIGHT_UP:
                player.add_event(LEFT_DOWN)

    def do(player):
        # === 발판이 없을 때 낙하 시작
        # 충돌 체크 (아래에 발판이 없는지 확인)
        collipse = False

        for obj in game_world.all_objects():
            if obj.__class__ == Map_Box.Box_Question \
                    or obj.__class__ == Map_Brick.Brick \
                    or obj.__class__ == Map_Pipe.Pipe \
                    or obj.__class__ == Map_Tile.Tile\
                    or obj.__class__ == Map_MovingTile.MovingTile\
                    or obj.__class__ == Map_Bridge.BridgeBoom\
                    or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:  # 충돌체크를 해야할 클래스의 이름
                if collideCheck(player, obj) == "bottom":
                    collipse = True
                    break

        if not collipse:
            player.add_event(FALLING_EVENT)

    def draw(player):
        player.image.clip_draw(0, player.imageH - player.frameY
                               , player.frameX, player.frameY, player.x - player.scrollX, player.y)


class RunState:

    def enter(player, event):
        player.velocity = 0

        if event == RIGHT_DOWN:
            player.dir = 1
        elif event == LEFT_DOWN:
            player.dir = -1
        elif event == RIGHT_UP:
            player.dir = -1
        elif event == LEFT_UP:
            player.dir = 1

        player.velocity += player.dir * RUN_SPEED_PPS


    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

        if event == RIGHT_DOWN or event == LEFT_DOWN:
            player.isDoubleInput = True

        if event == UP_DOWN or event == FALLING_EVENT:
            player.isMovingInAir = True

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        #=== x 이동
        # 충돌 체크 (왼쪽 or 오른쪽이이 오브젝트로 혀있는지 확인)
        collipse = False

        for obj in game_world.all_objects():
            if obj.__class__ == Map_Box.Box_Question \
                    or obj.__class__ == Map_Brick.Brick \
                    or obj.__class__ == Map_Pipe.Pipe \
                    or obj.__class__ == Map_Tile.Tile\
                    or obj.__class__ == Map_MovingTile.MovingTile\
                    or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:  # 충돌체크를 해야할 클래스의 이름
                if collideCheck(player, obj) == "left":
                    collipse = True
                    player.x = obj.x + obj.frameX / 2 + player.frameX / 2 + 1
                    break
                elif collideCheck(player, obj) == "right":
                    collipse = True
                    player.x = obj.x - obj.frameX / 2 - player.frameX / 2 - 1
                    break

        # 충돌하지 않았을 때에만 이동
        if not collipse:
            player.x += player.velocity * game_framework.frame_time
            player.x = clamp(25, player.x, 6600 - 25)


        #=== 발판이 없을 때 낙하 시작
        # 충돌 체크 (아래에 발판이 없는지 확인)
        collipse = False

        for obj in game_world.all_objects():
            if obj.__class__ == Map_Box.Box_Question \
                    or obj.__class__ == Map_Brick.Brick \
                    or obj.__class__ == Map_Pipe.Pipe \
                    or obj.__class__ == Map_Tile.Tile\
                    or obj.__class__ == Map_MovingTile.MovingTile\
                    or obj.__class__ == Map_Bridge.BridgeBoom\
                    or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:  # 충돌체크를 해야할 클래스의 이름
                if collideCheck(player, obj) == "bottom":
                    collipse = True
                    break

        if not collipse:
            player.add_event(FALLING_EVENT)

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Run
                               ,player.frameX, player.frameY, player.x - player.scrollX, player.y)


class DashState:

    def enter(player, event):
        player.velocity = 0

        if not player.isDash:
            player.isDash = True

        if event == RIGHT_DOWN:
            player.dir = 1
        elif event == LEFT_DOWN:
            player.dir = -1
        elif event == RIGHT_UP:
            player.dir = -1
        elif event == LEFT_UP:
            player.dir = 1

        player.velocity += player.dir * DASH_SPEED_PPS

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

        if event == UP_DOWN or event == FALLING_EVENT:
            player.isMovingInAir = True

        if event == SHIFT_UP:
            player.isDash = False

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        #=== x 이동
        # 충돌 체크 (왼쪽 or 오른쪽이이 오브젝트로 혀있는지 확인)
        collipse = False
        for obj in game_world.all_objects():
            if obj.__class__ == Map_Box.Box_Question \
                    or obj.__class__ == Map_Brick.Brick \
                    or obj.__class__ == Map_Pipe.Pipe \
                    or obj.__class__ == Map_Tile.Tile\
                    or obj.__class__ == Map_MovingTile.MovingTile\
                    or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:  # 충돌체크를 해야할 클래스의 이름
                if collideCheck(player, obj) == "left":
                    collipse = True
                    player.x = obj.x + obj.frameX / 2 + player.frameX / 2 + 1
                    break
                elif collideCheck(player, obj) == "right":
                    collipse = True
                    player.x = obj.x - obj.frameX / 2 - player.frameX / 2 - 1
                    break

        # 충돌하지 않았을 때에만 이동
        if not collipse:
            player.x += player.velocity * game_framework.frame_time
            player.x = clamp(25, player.x, 6600 - 25)


        #=== 발판이 없을 때 낙하 운동
        # 충돌 체크 (아래에 발판이 없는지 확인)
        collipse = False

        for obj in game_world.all_objects():
            if obj.__class__ == Map_Box.Box_Question \
                    or obj.__class__ == Map_Brick.Brick \
                    or obj.__class__ == Map_Pipe.Pipe \
                    or obj.__class__ == Map_Tile.Tile\
                    or obj.__class__ == Map_MovingTile.MovingTile\
                    or obj.__class__ == Map_Bridge.BridgeBoom\
                    or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:  # 충돌체크를 해야할 클래스의 이름
                if collideCheck(player, obj) == "bottom":
                    player.y = obj.y + obj.frameY/2 + player.frameY/2  # 발판 위로 올림
                    collipse = True
                    break

        if not collipse:
            player.add_event(FALLING_EVENT)

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Dash
                               ,player.frameX, player.frameY, player.x - player.scrollX, player.y)


class DownState:

    def enter(player, event):
        player.velocity = 0
        player.frame = 0

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Down
                               ,player.frameX, player.frameY, player.x - player.scrollX, player.y)


class JumpState:
    def enter(player, event):
        player.frame = 0
        player.velocity = 0

        if not player.isJumping:
            player.timer_jump = 0
            player.jump_startY = player.y
            player.isJumping = True

        # 방향
        if event == RIGHT_DOWN:
            player.isMovingInAir = True
            player.dir = 1
        elif event == LEFT_DOWN:
            player.isMovingInAir = True
            player.dir = -1

        # 속도
        if player.isDash:
            player.velocity += player.dir * DASH_SPEED_PPS
        else:
            player.velocity += player.dir * RUN_SPEED_PPS

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

        if event == RIGHT_UP or event == LEFT_UP:
            player.isMovingInAir = False

        if event == SHIFT_UP:
            player.isDash = False

        if event == UP_UP:
            collipse = False
            vel_jump = 0
            player.timer_jump = 0

        if event == FALLING_EVENT:
            collipse = False
            vel_jump = 0
            player.timer_jump = 0

        if event == DOWN_DOWN:
            collipse = False
            vel_jump = 0
            player.timer_jump = 0

    def do(player):
        #=== 점프 중 이동
        player.timer_jump += game_framework.frame_time

        #== x축 이동
        if player.isMovingInAir:
            # 충돌 체크 (왼쪽 or 오른쪽이이 오브젝트로 혀있는지 확인)
            collipse = False
            for obj in game_world.all_objects():
                if obj.__class__ == Map_Box.Box_Question \
                        or obj.__class__ == Map_Brick.Brick \
                        or obj.__class__ == Map_Pipe.Pipe \
                        or obj.__class__ == Map_Tile.Tile\
                        or obj.__class__ == Map_MovingTile.MovingTile\
                        or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:  # 충돌체크를 해야할 클래스의 이름
                    if collideCheck(player, obj) == "left":
                        collipse = True
                        player.x = obj.x + obj.frameX / 2 + player.frameX / 2 + 1
                        break
                    elif collideCheck(player, obj) == "right":
                        collipse = True
                        player.x = obj.x - obj.frameX / 2 - player.frameX / 2 - 1
                        break

            # 충돌하지 않았을 때에만 이동
            if not collipse:
                player.x += player.velocity * game_framework.frame_time
                player.x = clamp(25, player.x, 6600 - 25)

        #== y축 이동
        vel_jump = JUMP_V0_PPS + GRAVITY_ACCEL_PPS2 * player.timer_jump   # v = v0 + at

        # 위치
        # v(속도) = v0 + at --(적분)--> s(위치) = (1/2 at + v)t + s0
        player.y = ((1/2) * GRAVITY_ACCEL_PPS2 * player.timer_jump + JUMP_V0_PPS) * player.timer_jump + player.jump_startY

        # print('V = ' + str(vel_jump) + ', yPos = ' + str(player.y) + ', time = ' + str(player.timer_jump))

        # 상태 별 행동
        #=== 충돌 체크
        collipse = False

        # 점프 중 player의 윗부분 충돌
        for obj in game_world.all_objects():
            if obj.__class__ == Map_Box.Box_Question:  # 충돌체크를 해야할 클래스의 이름
                if collideCheck(player, obj) == "top":
                     # 충돌한 박스가 충돌하면 아이템이 나오는 question box 인 경우.
                    if not obj.isUsed:
                        if obj.itemValue == Map_Box.boxType.coin:
                            # 코인(이펙트) 생성
                            newCoin = Item_Coin.Coin()
                            newCoin.x, newCoin.y = obj.x, obj.y + obj.frameY/2 + 15
                            newCoin.isEffect = True
                            game_world.add_object(newCoin, 0)
                            game_data.gameData.score += 200
                            game_data.gameData.coin += 1
                        elif obj.itemValue == Map_Box.boxType.mushroom:
                            newMush = Item_TransForm.TransformItem()
                            newMush.x, newMush.y = obj.x, obj.y + obj.frameY
                            newMush.itemValue = Item_TransForm.Value.Mushroom
                            game_world.add_object(newMush, 1)
                        elif obj.itemValue == Map_Box.boxType.flower:
                            newFlower = Item_TransForm.TransformItem()
                            newFlower.x, newFlower.y = obj.x, obj.y + obj.frameY
                            newFlower.isReverse = False
                            newFlower.itemValue = Item_TransForm.Value.Fireflower
                            game_world.add_object(newFlower, 1)
                        # Box를 사용한 상태로 변경
                        obj.isUsed = True

                    # 충돌 상태 True
                    obj.slowFrame = 0
                    obj.frame = 0
                    collipse = True
                    break
            elif obj.__class__ == Map_Brick.Brick:
                if collideCheck(player, obj) == "top":
                    if int(player.transform) >= int(P_Transform.T_Super):
                        game_data.gameData.score += 100
                        game_world.remove_object(obj)
                    else:
                        print('col')
                        obj.nonDestroyCollide = True

                    collipse = True
                    break
            elif obj.__class__ == Map_Pipe.Pipe \
                    or obj.__class__ == Map_Tile.Tile\
                    or obj.__class__ == Map_MovingTile.MovingTile\
                    or obj.__class__ == Map_Bridge.BridgeBoom\
                    or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:  # 충돌체크를 해야할 클래스의 이름
                if collideCheck(player, obj) == "top":
                    collipse = True
                    break

        # 점프 도중 player의 윗부분이 충돌했을 때
        if collipse:
            player.add_event(FALLING_EVENT)
        else:
            #===변곡점을 지나면 도약 상태에서 낙하 상태로 변경
            if vel_jump <= 0:
                player.add_event(FALLING_EVENT)

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Jump,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)


class FallingState:

    def enter(player, event):
        player.frame = 0

        if not player.isSave_startFallingPos:
            player.timer_jump = 0
            player.pos_startFalling = player.y
            player.isSave_startFallingPos = True

        # 방향
        if event == RIGHT_DOWN:
            player.isMovingInAir = True
            player.dir = 1
        elif event == LEFT_DOWN:
            player.isMovingInAir = True
            player.dir = -1

        # 속도
        if player.isDash:
            player.velocity = player.dir * DASH_SPEED_PPS
        else:
            player.velocity = player.dir * RUN_SPEED_PPS


    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

        if event == RIGHT_UP or event == LEFT_UP:
            player.isMovingInAir = False

        if event == SHIFT_UP:
            player.isDash = False

        if event == LANDING_EVENT or event == LANDING_RUN_EVENT or event == LANDING_DASH_EVENT:
            # 초기화
            player.timer_jump = 0
            player.isJumping = False
            player.isDash = False
            player.pos_startFalling = 0
            player.isSave_startFallingPos = False
            collipse = False

        if event == DOWN_DOWN:
            # 초기화
            player.timer_jump = 0
            player.isJumping = False
            player.pos_startFalling = 0
            player.isSave_startFallingPos = False
            collipse = False

    def do(player):
        # === 발판이 없을 때 낙하 운동
        # 충돌 체크 (아래에 발판이 없는지 확인)
        collipse = False

        for obj in game_world.all_objects():
            if obj.__class__ == Map_Box.Box_Question\
                    or obj.__class__ == Map_Brick.Brick\
                    or obj.__class__ == Map_Pipe.Pipe\
                    or obj.__class__ == Map_Tile.Tile\
                    or obj.__class__ == Map_MovingTile.MovingTile\
                    or obj.__class__ == Map_Bridge.BridgeBoom\
                    or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:      # 충돌체크를 해야할 클래스의 이름
                if collideCheck(player, obj) == "bottom":
                    player.y = obj.y + obj.frameY / 2 + player.frameY / 2
                    collipse = True
                    break

        if not collipse:
            #=== 이동
            player.timer_jump += game_framework.frame_time

            # 낙하 (수직낙하운동)
            # v = v0 + gt, v0 = 0 -> v = gt 에서
            # v = gt --(적분)--> S = 1/2 g t^2 + C (C = S0)  (*Game Design 폴더 참고)
            player.y = (1/2) * GRAVITY_ACCEL_PPS2 * (player.timer_jump ** 2) + player.pos_startFalling

            # x축 이동
            if player.isMovingInAir:
                # x축 이동
                if player.isMovingInAir:
                    # 충돌 체크 (왼쪽 or 오른쪽이이 오브젝트로 혀있는지 확인)
                    collipse = False
                    for obj in game_world.all_objects():
                        if obj.__class__ == Map_Box.Box_Question \
                                or obj.__class__ == Map_Brick.Brick \
                                or obj.__class__ == Map_Pipe.Pipe \
                                or obj.__class__ == Map_Tile.Tile\
                                or obj.__class__ == Map_MovingTile.MovingTile\
                                or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:  # 충돌체크를 해야할 클래스의 이름
                            if collideCheck(player, obj) == "left":
                                collipse = True
                                player.x = obj.x + obj.frameX / 2 + player.frameX / 2 + 1
                                break
                            elif collideCheck(player, obj) == "right":
                                collipse = True
                                player.x = obj.x - obj.frameX / 2 - player.frameX / 2 - 1
                                break

                    # 충돌하지 않았을 때에만 이동
                    if not collipse:
                        player.x += player.velocity * game_framework.frame_time
                        player.x = clamp(25, player.x, 6600 - 25)

        else:
            # 다음 상태 지정
            if player.isMovingInAir:
                if player.isDash:
                    player.add_event(LANDING_DASH_EVENT)
                else:
                    player.add_event(LANDING_RUN_EVENT)
            else:
                player.add_event(LANDING_EVENT)

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Jump,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)


class GroundpoundState:
    def enter(player, event):
        player.frame = 0
        player.velocity = 0

        # 점프에 필요했던 변수들 초기화
        if player.isJumping: player.isJumping = False
        if player.isMovingInAir: player.isMovingInAir = False
        player.timer_jump = 0

        # 기타 변수들 초기화
        if player.isDash: player.isDash = False


    def exit(player, event):
        if event == LANDING_EVENT:
            player.isJumping = False
            player.timer_jump = 0
            collipse = False

    def do(player):
        # 아래로 빠르게 낙하
        player.timer_jump += game_framework.frame_time
        player.timer_jump = clamp(0, player.timer_jump, 0.2)

        player.y += (1/2) * GRAVITY_ACCEL_PPS2 * (player.timer_jump ** 2)

        # print('V = ' + str(vel_jump) + ', yPos = ' + str(player.y) + ', time = ' + str(player.timer_jump))

        collipse = False
        checkCount = 0
        # 충돌해서 착지를 할 때
        while (not collipse and checkCount < 4):
            if checkCount == 0:
                for obj in game_world.all_objects():
                    if obj.__class__ == Map_Box.Box_Question:
                        if collideCheck(player, obj) == "bottom":
                            player.y = obj.y + obj.frameY / 2 + player.frameY / 2
                            collipse = True

                            # 충돌한 박스가 충돌하면 아이템이 나오는 question box 인 경우.
                            if not obj.isUsed:
                                if obj.itemValue == Map_Box.boxType.coin:
                                    # 코인(이펙트) 생성
                                    newCoin = Item_Coin.Coin()
                                    newCoin.x, newCoin.y = obj.x, obj.y - obj.frameY/2 - 15
                                    newCoin.isEffect = True
                                    game_world.add_object(newCoin, 0)
                                    game_data.gameData.score += 200
                                    game_data.gameData.coin += 1
                                elif obj.itemValue == Map_Box.boxType.mushroom:
                                    newMush = Item_TransForm.TransformItem()
                                    newMush.x, newMush.y = obj.x, obj.y - obj.frameY
                                    newMush.itemValue = Item_TransForm.Value.Mushroom
                                    game_world.add_object(newMush, 1)
                                elif obj.itemValue == Map_Box.boxType.flower:
                                    newFlower = Item_TransForm.TransformItem()
                                    newFlower.x, newFlower.y = obj.x, obj.y - obj.frameY
                                    newFlower.isReverse = True
                                    newFlower.itemValue = Item_TransForm.Value.Fireflower
                                    game_world.add_object(newFlower, 1)

                                # Box를 사용한 상태로 변경
                                obj.isUsed = True
                            break
                    elif obj.__class__ == Map_Brick.Brick:
                        if int(player.transform) >= int(P_Transform.T_Super):
                            if collideCheck(player, obj) == "bottom":
                                game_data.gameData.score += 100
                                game_world.remove_object(obj)
                                collipse = True
                                break
                    elif obj.__class__ == Map_Pipe.Pipe \
                            or obj.__class__ == Map_Tile.Tile\
                            or obj.__class__ == Map_MovingTile.MovingTile\
                            or obj.__class__ == Map_Bridge.BridgeBoom\
                            or obj.__class__ == Obstacle_Rotatedfire_Center.RotatedfireCenter:  # 충돌체크를 해야할 클래스의 이름
                        if collideCheck(player, obj) == "bottom":
                            player.y = obj.y + obj.frameY/2 + player.frameY/2  # 발판 위로 올림
                            collipse = True
                            break

            checkCount += 1

        if collipse:
            player.add_event(LANDING_EVENT)


    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_GP
                               ,player.frameX, player.frameY, player.x - player.scrollX, player.y)


class TranslateState:
    def enter(player, event):
        if player.isTrans:                          # 한 번만 수행되도록
            player.frame = 0
            player.isTrans = False

        if event == SHIFT_UP:                       # 변신 도중 SHIFT키를 떼었을 때
            player.isDash = False
            player.prevState = "RunState"

        if event == LEFT_UP or event == RIGHT_UP:   # 변신 도중 왼쪽or오른쪽 키를 떼었을 때
            player.isMovingInAir = False
            player.prevState = "IdleState"

        if player.transform == P_Transform.T_Basic:
            player.jump_startY = player.y


    def exit(player, event):
        if event == TRANS2IDLE_EVENT or event == TRANS2RUN_EVENT or event == TRANS2DASH_EVENT:
            player.prevState = None
            player.isTrans = True

    def do(player):
        if player.transform == P_Transform.T_Basic:
            player.trans_timer += game_framework.frame_time
            # print('game over')
            # == y축 이동 ( 위로 올라갔다가 아래로 떨어지는 연출 )
            vel_jump = JUMP_V0_PPS + GRAVITY_ACCEL_PPS2 * player.trans_timer  # v = v0 + at

            # 위치
            # v(속도) = v0 + at --(적분)--> s(위치) = (1/2 at + v)t + s0
            player.y = ((1/2) * GRAVITY_ACCEL_PPS2 * player.trans_timer + JUMP_V0_PPS) * player.trans_timer + player.jump_startY

            if player.y <= 0 or player.trans_timer >= 3.0:
                player.jump_startY = 0
                player.trans_timer = 0
                player.transform = -1
        else:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
            if player.frame >= 5:
                player.frame = 0
                if player.prevState == "RunState":
                    player.add_event(TRANS2RUN_EVENT)
                elif player.prevState == "DashState":
                    player.add_event(TRANS2DASH_EVENT)
                else:
                    player.add_event(TRANS2IDLE_EVENT)


    def draw(player):
        if player.transform == P_Transform.T_Basic:
            player.image.clip_draw(0, 0, player.frameX, player.frameY
                                   , player.x - player.scrollX, player.y)
        else:
            player.image.clip_draw(int(player.frame) * player.frameX, 0, player.frameX, player.frameY
                                   , player.x - player.scrollX, player.y)


class HitState:
    def enter(player, event):
        if player.isTrans:                          # 한 번만 수행되도록
            player.frame = 0
            player.isTrans = False

        if event == SHIFT_UP:                       # 변신 도중 SHIFT키를 떼었을 때
            player.isDash = False
            player.prevState = "RunState"

        if event == LEFT_UP or event == RIGHT_UP:   # 변신 도중 왼쪽or오른쪽 키를 떼었을 때
            player.isMovingInAir = False
            player.prevState = "IdleState"


    def exit(player, event):
        if event == HIT2IDLE_EVENT or event == HIT2RUN_EVENT or event == HIT2DASH_EVENT:
            player.prevState = None
            player.isTrans = True

    def do(player):
        player.hit_timer += game_framework.frame_time
        if player.hit_timer >= 0.5: # 0.3초의 경직
            player.hit_timer = 0
            if player.prevState == "RunState":
                player.add_event(HIT2RUN_EVENT)
            elif player.prevState == "DashState":
                player.add_event(HIT2DASH_EVENT)
            else:
                player.add_event(HIT2IDLE_EVENT)


    def draw(player):
        player.image.clip_draw(0, player.imageH - player.frameY * P_State.S_Hit
                               , player.frameX, player.frameY, player.x - player.scrollX, player.y)


class StageclearState:

    def enter(player, event):
        if not player.stageclear:
            player.frame = 0
            #=== x 축 이동 관련
            player.dir = 1

            player.velocity = player.dir * RUN_SPEED_PPS

            #=== y 축 이동 관련
            player.timer_jump = 0
            player.pos_startFalling = player.y

            player.stageclear = True


    def exit(player, event):
        pass

    def do(player):
        #=== 공중에서 깃발과 충돌했다면 y 축 이동을 먼저 한다.
        # 충돌 체크 (아래에 발판이 없는지 & 현재 깃발과 충돌중인지 확인)
        collipse = False
        player_in_flag = True

        for obj in game_world.all_objects():
            if obj.__class__ == Map_Tile.Tile:
                if collideCheck(player, obj) == 'bottom':
                    player.y = obj.y + obj.frameY / 2 + player.frameY / 2
                    collipse = True
                    player_in_flag = False
                    break

        if not collipse:
            player.frame = 0
            # 낙하 (수직낙하운동, FallState 와 동일한 로직)
            player.timer_jump += game_framework.frame_time
            player.y = (1/2) * GRAVITY_ACCEL_PPS2 * (player.timer_jump ** 2) + player.pos_startFalling


        # x축 이동
        if not player_in_flag:
            collipse = False
            for obj in game_world.all_objects():
                if obj.__class__ == Map_Castle.Door or obj.__class__ == Npc_Kinopio.Kinopio:
                    if collideCheck(player, obj) == 'left':
                        player.y = obj.y - obj.frameY / 2 - player.frameY / 2
                        collipse = True
                        break

            if not collipse:
                player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
                #=== 자동으로 x 축 이동을 한다.
                player.x += player.velocity * game_framework.frame_time
                player.x = clamp(25, player.x, 6600 - 25)

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Run,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)



next_state_table = {
    IdleState: {RIGHT_DOWN: RunState, LEFT_DOWN: RunState, RIGHT_UP: IdleState, LEFT_UP: IdleState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: IdleState, SHIFT_UP: IdleState
        , SPACE: IdleState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState
        , STAGECLEAR_EVENT: StageclearState
        , HIT_EVENT: HitState},
    RunState: {RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, LEFT_UP: IdleState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: DashState, SHIFT_UP: RunState
        , SPACE: RunState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState
        , STAGECLEAR_EVENT: StageclearState
        , HIT_EVENT: HitState},
    DashState: {RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, LEFT_UP: IdleState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: RunState, SHIFT_UP: RunState
        , SPACE: DashState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState
        , STAGECLEAR_EVENT: StageclearState
        , HIT_EVENT: HitState},
    DownState: {RIGHT_DOWN: DownState, LEFT_DOWN: DownState, RIGHT_UP: DownState, LEFT_UP: DownState
        , UP_DOWN: DownState, UP_UP: DownState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: DownState, SHIFT_UP: DownState
        , SPACE: DownState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState
        , STAGECLEAR_EVENT: StageclearState
        , HIT_EVENT: HitState},
    JumpState: {RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState, RIGHT_UP: JumpState, LEFT_UP: JumpState
        , UP_DOWN: JumpState, UP_UP: FallingState, DOWN_DOWN: GroundpoundState, DOWN_UP: JumpState
        , SHIFT_DOWN: JumpState, SHIFT_UP: JumpState
        , SPACE: JumpState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState
        , STAGECLEAR_EVENT: StageclearState
        , HIT_EVENT: HitState},
    FallingState: {RIGHT_DOWN: FallingState, LEFT_DOWN: FallingState, RIGHT_UP: FallingState, LEFT_UP: FallingState
        , UP_DOWN: FallingState, UP_UP: FallingState, DOWN_DOWN: GroundpoundState, DOWN_UP: FallingState
        , SHIFT_DOWN: FallingState, SHIFT_UP: FallingState
        , SPACE: FallingState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState
        , STAGECLEAR_EVENT: StageclearState
        , HIT_EVENT: HitState},
    GroundpoundState: {RIGHT_DOWN: GroundpoundState, LEFT_DOWN: GroundpoundState, RIGHT_UP: GroundpoundState, LEFT_UP: GroundpoundState
        , UP_DOWN: GroundpoundState, UP_UP: GroundpoundState, DOWN_DOWN: GroundpoundState, DOWN_UP: GroundpoundState
        , SHIFT_DOWN: GroundpoundState, SHIFT_UP: GroundpoundState
        , SPACE: GroundpoundState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState
        , STAGECLEAR_EVENT: StageclearState
        , HIT_EVENT: HitState},
    TranslateState: {RIGHT_DOWN: TranslateState, LEFT_DOWN: TranslateState, RIGHT_UP: TranslateState, LEFT_UP: TranslateState
        , UP_DOWN: TranslateState, UP_UP: TranslateState, DOWN_DOWN: TranslateState, DOWN_UP: TranslateState
        , SHIFT_DOWN: TranslateState, SHIFT_UP: TranslateState
        , SPACE: TranslateState
        , FALLING_EVENT: TranslateState
        , LANDING_EVENT: TranslateState, LANDING_RUN_EVENT: TranslateState, LANDING_DASH_EVENT: TranslateState
        , TRANSLATE_EVENT: IdleState, TRANS2IDLE_EVENT: IdleState, TRANS2RUN_EVENT: RunState, TRANS2DASH_EVENT: DashState, TRANS2JUMP: JumpState
        , STAGECLEAR_EVENT: StageclearState
        , HIT_EVENT: HitState},
    StageclearState: {RIGHT_DOWN: StageclearState, LEFT_DOWN: StageclearState, RIGHT_UP: StageclearState, LEFT_UP: StageclearState
        , UP_DOWN: StageclearState, UP_UP: StageclearState, DOWN_DOWN: StageclearState, DOWN_UP: StageclearState
        , SHIFT_DOWN: StageclearState, SHIFT_UP: StageclearState
        , SPACE: StageclearState
        , FALLING_EVENT: StageclearState
        , LANDING_EVENT: StageclearState, LANDING_RUN_EVENT: StageclearState, LANDING_DASH_EVENT: StageclearState
        , TRANSLATE_EVENT: StageclearState, TRANS2IDLE_EVENT: StageclearState, TRANS2RUN_EVENT: StageclearState, TRANS2DASH_EVENT: StageclearState, TRANS2JUMP: StageclearState
        , STAGECLEAR_EVENT: StageclearState},
    HitState: {RIGHT_DOWN: HitState, LEFT_DOWN: HitState, RIGHT_UP: HitState, LEFT_UP: HitState
        , UP_DOWN: HitState, UP_UP: HitState, DOWN_DOWN: HitState, DOWN_UP: HitState
        , SHIFT_DOWN: HitState, SHIFT_UP: HitState
        , SPACE: HitState
        , FALLING_EVENT: HitState
        , LANDING_EVENT: HitState, LANDING_RUN_EVENT: HitState, LANDING_DASH_EVENT: HitState
        , TRANSLATE_EVENT: IdleState, TRANS2IDLE_EVENT: IdleState, TRANS2RUN_EVENT: RunState, TRANS2DASH_EVENT: DashState, TRANS2JUMP: JumpState
        , HIT2IDLE_EVENT: IdleState, HIT2RUN_EVENT: RunState, HIT2DASH_EVENT: DashState, HIT2JUMP_EVENT: JumpState
        , STAGECLEAR_EVENT: StageclearState
        , HIT_EVENT: HitState},
}

# HIT_EVENT
class Player:
    image_StandardL = None
    def __init__(self):
        # position
        self.x, self.y = 100, 60
        self.frameX, self.frameY = 30, 30
        self.imageH = 300

        # Scroll
        self.scrollX = 0

        # Image Loading
        if self.image_StandardL == None:
            self.image_StandardL = load_image('MarioL.png')
            self.image_StandardR = load_image('Mario.png')
            self.image_SuperL = load_image('MarioL_super.png')
            self.image_SuperR = load_image('Mario_super.png')
            self.image_FireL = load_image('MarioL_fire.png')
            self.image_FireR = load_image('Mario_fire.png')

            self.image = self.image_StandardL

        self.transform = P_Transform.T_Basic
        self.prevState = None  # 이전상태의 이름
        self.isTrans = False   # 변신 중 인지

        self.never_collide_with_mob = False   # 몹과는 절대로 충돌하지 않는상태
        self.ncwmTimer = 0                    # 충돌하지 않는 상태 타이머

        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer_jump = 0         # 점프 타이머
        self.jump_startY = 0        # 점프를 시작한 y좌표
        self.isJumping = False      # 점프

        self.isSave_startFallingPos = False # pos_startFalling를 저장했는 지 #test
        self.pos_startFalling = 0           # 발판이 없을 때 낙하를 시작하는 좌표 #test

        self.isCollideJumping = False       # 점프 중에 충돌했는 지
        self.pos_collideJumping = 0         # 점프 중에 충돌한 시점의 좌표
        self.time_collideJumping = 0        # 점프 중에 충돌한 시점의 시점

        self.isMovingInAir = False  # 공중에서 움직이는지
        self.isDoubleInput = False  # 키입력이 두 개 동시에 되었는지
        self.isDash = False         # 대쉬 중인지

        self.trans_timer = 0
        self.hit_timer = 0

        self.once = False

        self.show_bb = False  # 바운딩박스 출력

        self.stageclear = False     # stage를 클리어했는지

        self.collide_trigger = False    # Trigger와 충돌했는지

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        # Debug #
        self.font = load_font('ENCR10B.TTF', 16)
        ###


    def fire_ball(self):
        # print(self.transform)
        # if self.transform == P_Transform.T_Fire:
        newFireball = ball.Fireball()
        newFireball.x, newFireball.y = self.x, self.y
        ball.fireballs.append(newFireball)
        game_world.add_object(newFireball, 1)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        # 이미지 업데이트
        if self.transform == P_Transform.T_Basic:
            if self.dir == 1:
                self.image = self.image_StandardR
            else:
                self.image = self.image_StandardL
        elif self.transform == P_Transform.T_Super:
            if self.dir == 1:
                self.image = self.image_SuperR
            else:
                self.image = self.image_SuperL
        elif self.transform == P_Transform.T_Fire:
            if self.dir == 1:
                self.image = self.image_FireR
            else:
                self.image = self.image_FireL

        # 충돌 관련
        # if self.y <= 0:
        #     self.transform = P_Transform.T_Basic
        #     game_data.gameData.transform = game_data.P_Transform.T_Basic
        #     self.add_event(TRANSLATE_EVENT)

        for obj in game_world.all_objects():
            # 움직이는 발판
            if obj.__class__ == Map_MovingTile.MovingTile:
                if collideCheck(self, obj) == 'bottom':
                    if obj.ver_or_hor == 'vertical':
                        self.y += obj.dir * Map_MovingTile.MOVE_SPEED_PPS * game_framework.frame_time
                    elif obj.ver_or_hor == 'horizontal':
                        self.y = obj.y + obj.frameY/2 + self.frameY/2

            # 변신 아이템 충돌
            if obj.__class__ == Item_TransForm.TransformItem:  # 충돌체크를 해야할 클래스의 이름
                if not collideCheck(self, obj) == None:
                    game_data.gameData.score += 1000
                    if self.transform < obj.itemValue:
                        self.prevState = self.cur_state.__name__  # 이전상태의 이름을 저장해둔다.
                        if not self.cur_state == JumpState or self.cur_state == GroundpoundState: #버그방지용
                            self.y += 15

                        if obj.itemValue == Item_TransForm.Value.Mushroom:
                            self.transform = P_Transform.T_Super
                        elif obj.itemValue == Item_TransForm.Value.Fireflower:
                            self.transform = P_Transform.T_Fire
                        game_data.gameData.transform = self.transform   # 게임데이터 최신화
                        # Frame Image Update
                        self.frameX, self.frameY = 30, 60
                        self.imageH = 600
                        self.add_event(TRANSLATE_EVENT)

                    # 해당 충돌 아이템 삭제
                    game_world.remove_object(obj)
                    break
            if obj.__class__ == Item_Coin.Coin:
                if not obj.isEffect:
                    if not collideCheck(self, obj) == None:
                        game_data.gameData.coin += 1
                        game_world.remove_object(obj)
                        break

        #=== 몬스터
        if self.never_collide_with_mob: # 무적시간
            self.ncwmTimer -= game_framework.frame_time
            print(self.ncwmTimer)
            if self.ncwmTimer <= 0:
                self.never_collide_with_mob = False
        # goomba
        for mob in game_world.all_objects():
            if mob.__class__ == mob_goomba.Goomba:  # 충돌체크를 해야할 클래스의 이름
                if not mob.ismoving:
                    # goomba는 화면에 처음 잡혔을 때부터 움직이기 시작한다.
                    if self.x <= mob.x <= self.x + 800:
                        mob.ismoving = True
                else:
                    # goomba의 시야에 플레이어가 들어오면 돌진을 시작한다.
                    if mob.dir == 1:
                        if mob.x < self.x < mob.x + 300:
                            mob.state = mob_goomba.G_State.Dash
                        else:
                            mob.state = mob_goomba.G_State.Walk
                    else:
                        if mob.x - 300 < self.x < mob.x:
                            mob.state = mob_goomba.G_State.Dash
                        else:
                            mob.state = mob_goomba.G_State.Walk

                    # 충돌체크
                    if not collideCheck(self, mob) == None:
                        if self.cur_state == FallingState or self.cur_state == GroundpoundState:
                            if collideCheck(self, mob) == 'bottom':
                                # 충돌한 객체 삭제
                                game_data.gameData.score += 100
                                game_world.remove_object(mob)
                        else:
                            if not self.never_collide_with_mob:
                                self.never_collide_with_mob = True  # 몹과 충돌하지 않는 상태가 되어서
                                self.ncwmTimer = 2.0               # 2초의 무적시간이 주어진다.

                                if self.transform == P_Transform.T_Basic:
                                    self.add_event(TRANSLATE_EVENT)
                                elif self.transform == P_Transform.T_Super:
                                    self.frameX, self.frameY = 30, 30
                                    self.imageH = 300
                                    self.transform = P_Transform.T_Basic
                                    game_data.gameData.transform = game_data.P_Transform.T_Basic
                                    self.add_event(HIT_EVENT)
                                elif self.transform == P_Transform.T_Fire:
                                    self.transform = P_Transform.T_Super
                                    game_data.gameData.transform = game_data.P_Transform.T_Super
                                    self.add_event(HIT_EVENT)

            elif mob.__class__ == Map_Lava.Lava:
                if not self.cur_state == TranslateState:
                    if not collideCheck(self, mob) == None:     # 용암에 충돌헀다면
                        self.transform = P_Transform.T_Basic
                        game_data.gameData.transform = game_data.P_Transform.T_Basic
                        self.add_event(TRANSLATE_EVENT)

            elif mob.__class__ == Obstacle_Rotatedfire.RotatedFire:     # 회전하는 불에 충돌하면
                if not collideCheck(self, mob) == None:
                    if not self.never_collide_with_mob:
                        self.never_collide_with_mob = True  # 몹과 충돌하지 않는 상태가 되어서
                        self.ncwmTimer = 2.0                # 2초의 무적시간이 주어진다.

                        if self.transform == P_Transform.T_Basic:
                            self.add_event(TRANSLATE_EVENT)
                        elif self.transform == P_Transform.T_Super:
                            self.frameX, self.frameY = 30, 30
                            self.imageH = 300
                            self.transform = P_Transform.T_Basic
                            game_data.gameData.transform = game_data.P_Transform.T_Basic
                            self.add_event(HIT_EVENT)
                        elif self.transform == P_Transform.T_Fire:
                            self.transform = P_Transform.T_Super
                            game_data.gameData.transform = game_data.P_Transform.T_Super
                            self.add_event(HIT_EVENT)

            elif mob.__class__ == mob_kupa.Kupa:
                if not collideCheck(self, mob) == None:
                    if collideCheck(self, mob) == 'bottom':
                        if not self.never_collide_with_mob:
                            if mob.state == mob_kupa.K_State.S_Hide:
                                pass
                            else:
                                self.never_collide_with_mob = True  # 몹과 충돌하지 않는 상태가 되어서
                                self.ncwmTimer = 1.3  # 1.3초의 무적시간이 주어진다.

                                self.cur_state = JumpState
                    else:
                        if not self.never_collide_with_mob:
                            self.never_collide_with_mob = True  # 몹과 충돌하지 않는 상태가 되어서
                            self.ncwmTimer = 2.0                # 2초의 무적시간이 주어진다.

                            if self.transform == P_Transform.T_Basic:
                                self.add_event(TRANSLATE_EVENT)
                            elif self.transform == P_Transform.T_Super:
                                self.frameX, self.frameY = 30, 30
                                self.imageH = 300
                                self.transform = P_Transform.T_Basic
                                game_data.gameData.transform = game_data.P_Transform.T_Basic
                                self.add_event(HIT_EVENT)
                            elif self.transform == P_Transform.T_Fire:
                                self.transform = P_Transform.T_Super
                                game_data.gameData.transform = game_data.P_Transform.T_Super
                                self.add_event(HIT_EVENT)



        #=== 스테이지 클리어 관련
        # Flag, Button
        for obj in game_world.all_objects():
            if obj.__class__ == Map_Flag.Bar:  # 충돌체크를 해야할 클래스의 이름
                if not collideCheck(self, obj) == None:
                    if not self.once:
                        if self.y < 200:
                            game_data.gameData.score += 1000
                        elif 200 <= self.y < 400:
                            game_data.gameData.score += 3000
                        elif self.y >= 400:
                            game_data.gameData.score += 5000

                        self.once = True

                    game_data.gameData.score += 200 * game_data.gameData.coin
                    game_data.gameData.coin = 0
                    self.add_event(STAGECLEAR_EVENT)
            if obj.__class__ == Obstacle_Button.BoomButton:
                if not collideCheck(self, obj) == None:
                    self.add_event(STAGECLEAR_EVENT)

        for trigger in Trigger.triggers:
            if trigger.type == "autoMoving":
                self.add_event(STAGECLEAR_EVENT)



    def get_boundingbox(self):  # 바운딩박스
        return self.x - self.frameX/2, self.y + self.frameY/2, self.x + self.frameX/2, self.y - self.frameY/2

    def draw(self):
        self.cur_state.draw(self)

        # bounding box
        if self.show_bb:
            draw_rectangle(self.x - self.frameX/2 - self.scrollX, self.y + self.frameY/2
                           , self.x + self.frameX/2 - self.scrollX, self.y - self.frameY/2)

        # Debug #
        # self.font.draw(self.x - 60 - self.scrollX, self.y + 70, 'State' + str(self.cur_state), (255, 255, 0))
        # self.font.draw(self.x - 60 - self.scrollX, self.y + 50, 'Dir ' + str(self.dir), (255, 255, 0))
        ###

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.collide_trigger:
                print('이동')  #
                self.x, self.y = 3435, 120

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_b):
            if self.show_bb:
                self.show_bb = False
                Map_Box.show_bb = False
                Map_Brick.show_bb = False
                Map_Pipe.show_bb = False
                Map_Tile.show_bb = False
                Item_TransForm.show_bb = False
                mob_goomba.show_bb = False
                Map_Castle.show_bb = False
                Trigger.show_bb = False
                Map_Flag.show_bb = False
                Map_MovingTile.show_bb = False
                Map_Lava.show_bb = False
                Obstacle_Rotatedfire.show_bb = False
                Map_Bridge.show_bb = False
                mob_kupa.show_bb = False
                mob_kupa_breath.show_bb = False
                Npc_Kinopio.show_bb = False
                Obstacle_Rotatedfire_Center.show_bb = False
                Obstacle_Button.show_bb = False
            else:
                self.show_bb = True
                Map_Box.show_bb = True
                Map_Brick.show_bb = True
                Map_Pipe.show_bb = True
                Map_Tile.show_bb = True
                Item_TransForm.show_bb = True
                mob_goomba.show_bb = True
                Map_Castle.show_bb = True
                Trigger.show_bb = True
                Map_Flag.show_bb = True
                Map_MovingTile.show_bb = True
                Map_Lava.show_bb = True
                Obstacle_Rotatedfire.show_bb = True
                Map_Bridge.show_bb = True
                mob_kupa.show_bb = True
                mob_kupa_breath.show_bb = False
                Npc_Kinopio.show_bb = True
                Obstacle_Rotatedfire_Center.show_bb = True
                Obstacle_Button.show_bb = True

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            score = game_data.gameData.score
            coin = game_data.gameData.coin
            life = game_data.gameData.life
            transform = game_data.gameData.transform
            print('Life: ' + str(life), ' | Score: ' + str(score)
                  + ' | Coin: ' + str(coin) + ' | Transform: ' + str(transform))

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_l):
            self.x += (-1) * self.dir * 10


def reset_variable(player):
    # position
    player.x, player.y = 100, 60

    # Scroll
    player.scrollX = 0

    player.prevState = None  # 이전상태의 이름
    player.isTrans = False  # 변신 중 인지

    player.never_collide_with_mob = False  # 몹과는 절대로 충돌하지 않는상태
    player.ncwmTimer = 0  # 충돌하지 않는 상태 타이머

    player.dir = 1
    player.velocity = 0
    player.frame = 0
    player.timer_jump = 0  # 점프 타이머
    player.jump_startY = 0  # 점프를 시작한 y좌표
    player.isJumping = False  # 점프

    player.isSave_startFallingPos = False  # pos_startFalling를 저장했는 지 #test
    player.pos_startFalling = 0  # 발판이 없을 때 낙하를 시작하는 좌표 #test

    player.isCollideJumping = False  # 점프 중에 충돌했는 지
    player.pos_collideJumping = 0  # 점프 중에 충돌한 시점의 좌표
    player.time_collideJumping = 0  # 점프 중에 충돌한 시점의 시점

    player.isMovingInAir = False  # 공중에서 움직이는지
    player.isDoubleInput = False  # 키입력이 두 개 동시에 되었는지
    player.isDash = False  # 대쉬 중인지

    player.show_bb = False  # 바운딩박스 출력

    player.stageclear = False  # stage를 클리어했는지

    player.cur_state = IdleState
    player.cur_state.enter(player, None)

def StageClearFunc(player):
    player.add_event(STAGECLEAR_EVENT)
