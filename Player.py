import game_framework
import enum
import math

import mob_goomba
from collide import *
from pico2d import *

import game_data
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe
import Map_Castle
import Item_Coin
import Item_TransForm
import ball

import game_world

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
    S_Idle = 0
    S_Run = enum.auto()
    S_Hit = enum.auto()
    S_Jump = enum.auto()
    S_Dash = enum.auto()
    S_Down = enum.auto()
    S_Slide = enum.auto()
    S_Stand = enum.auto()
    S_Kick = enum.auto()
    S_Climb = enum.auto()
    S_Gameover = enum.auto()
    S_Transform = enum.auto()


# Player Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP\
    ,UP_DOWN, DOWN_DOWN, UP_UP, DOWN_UP\
    ,SHIFT_DOWN, SHIFT_UP\
    ,SPACE\
    ,FALLING_EVENT, LANDING_EVENT, LANDING_RUN_EVENT, LANDING_DASH_EVENT\
    ,TRANSLATE_EVENT, TRANS2IDLE_EVENT, TRANS2RUN_EVENT, TRANS2DASH_EVENT, TRANS2JUMP = range(20)

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
        # 오랫동안 입력이 없을 때
        # player.timer -= 1
        # if player.timer == 0:
        #     player.add_event(SLEEP_TIMER)

        # === 발판이 없을 때 낙하 시작
        # 충돌 체크 (아래에 발판이 없는지 확인)
        collipse = False
        checkCount = 0

        while (not collipse and checkCount < 4):
            if checkCount == 0:
                for box in Map_Box.boxes:
                    if collideCheck(player, box) == "bottom":
                        collipse = True
                        break
            elif checkCount == 1:
                for brick in Map_Brick.bricks:
                    if collideCheck(player, brick) == "bottom":
                        collipse = True
                        break
            elif checkCount == 2:
                for pipe in Map_Pipe.pipes:
                    if collideCheck(player, pipe) == "bottom":
                        collipse = True
                        break
            elif checkCount == 3:
                for tile in Map_Tile.tiles:
                    if collideCheck(player, tile) == "bottom":
                        collipse = True
                        break

            checkCount += 1

        if not collipse:
            player.add_event(FALLING_EVENT)

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH, player.frameX, player.frameY
                               , player.x - player.scrollX, player.y)


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
        checkCount = 0
        while (not collipse and checkCount < 4):
            if checkCount == 0:
                for box in Map_Box.boxes:
                    if collideCheck(player, box) == "left" or collideCheck(player, box) == "right":
                        collipse = True
                        break
            elif checkCount == 1:
                for brick in Map_Brick.bricks:
                    if collideCheck(player, brick) == "left" or collideCheck(player, brick) == "right":
                        collipse = True
                        break
            elif checkCount == 2:
                for pipe in Map_Pipe.pipes:
                    if collideCheck(player, pipe) == "left" or collideCheck(player, pipe) == "right":
                        collipse = True
                        break
            elif checkCount == 3:
                for tile in Map_Tile.tiles:
                    if collideCheck(player, tile) == "left" or collideCheck(player, tile) == "right":
                        collipse = True
                        break

            checkCount += 1

        # 충돌하지 않았을 때에만 이동
        if not collipse:
            player.x += player.velocity * game_framework.frame_time
            player.x = clamp(25, player.x, 6600 - 25)


        #=== 발판이 없을 때 낙하 시작
        # 충돌 체크 (아래에 발판이 없는지 확인)
        collipse = False
        checkCount = 0
        while (not collipse and checkCount < 4):
            if checkCount == 0:
                for box in Map_Box.boxes:
                    if collideCheck(player, box) == "bottom":
                        collipse = True
                        break
            elif checkCount == 1:
                for brick in Map_Brick.bricks:
                    if collideCheck(player, brick) == "bottom":
                        collipse = True
                        break
            elif checkCount == 2:
                for pipe in Map_Pipe.pipes:
                    if collideCheck(player, pipe) == "bottom":
                        collipse = True
                        break
            elif checkCount == 3:
                for tile in Map_Tile.tiles:
                    if collideCheck(player, tile) == "bottom":
                        collipse = True
                        break

            checkCount += 1

        if not collipse:
            player.add_event(FALLING_EVENT)

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Run,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)


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
        checkCount = 0
        while (not collipse and checkCount < 4):
            if checkCount == 0:
                for box in Map_Box.boxes:
                    if collideCheck(player, box) == "left" or collideCheck(player, box) == "right":
                        collipse = True
                        break
            elif checkCount == 1:
                for brick in Map_Brick.bricks:
                    if collideCheck(player, brick) == "left" or collideCheck(player, brick) == "right":
                        collipse = True
                        break
            elif checkCount == 2:
                for pipe in Map_Pipe.pipes:
                    if collideCheck(player, pipe) == "left" or collideCheck(player, pipe) == "right":
                        collipse = True
                        break
            elif checkCount == 3:
                for tile in Map_Tile.tiles:
                    if collideCheck(player, tile) == "left" or collideCheck(player, tile) == "right":
                        collipse = True
                        break

            checkCount += 1

        # 충돌하지 않았을 때에만 이동
        if not collipse:
            player.x += player.velocity * game_framework.frame_time
            player.x = clamp(25, player.x, 6600 - 25)


        #=== 발판이 없을 때 낙하 운동
        # 충돌 체크 (아래에 발판이 없는지 확인)
        collipse = False
        checkCount = 0

        while (not collipse and checkCount < 4):
            if checkCount == 0:
                for box in Map_Box.boxes:
                    if collideCheck(player, box) == "bottom":
                        player.y = box.y + box.frameY/2 + player.frameY/2  # 발판 위로 올림
                        collipse = True
                        break
            elif checkCount == 1:
                for brick in Map_Brick.bricks:
                    if collideCheck(player, brick) == "bottom":
                        player.y = brick.y + brick.frameY/2 + player.frameY/2  # 발판 위로 올림
                        collipse = True
                        break
            elif checkCount == 2:
                for pipe in Map_Pipe.pipes:
                    if collideCheck(player, pipe) == "bottom":
                        player.y = pipe.y + pipe.frameY/2 + player.frameY/2  # 발판 위로 올림
                        collipse = True
                        break
            elif checkCount == 3:
                for tile in Map_Tile.tiles:
                    if collideCheck(player, tile) == "bottom":
                        player.y = tile.y + tile.frameY/2 + player.frameY/2  # 발판 위로 올림
                        collipse = True
                        break

            checkCount += 1

        if not collipse:
            if not player.isSave_startFallingPos:
                player.pos_startFalling = player.y
                player.isSave_startFallingPos = True

            # 낙하 (수직낙하운동)
            player.timer_jump += game_framework.frame_time
            # v = v0 + gt, v0 = 0 -> v = gt 에서
            # v = gt --(적분)--> S = 1/2 g t^2 + C (C = S0)  (*Game Design 폴더 참고)
            player.y = (1/2) * GRAVITY_ACCEL_PPS2 * (player.timer_jump ** 2) + player.pos_startFalling

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Dash,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)


class DownState:

    def enter(player, event):
        player.velocity = 0
        player.frame = 0

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Down,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)


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
            checkCount = 0
            while (not collipse and checkCount < 4):
                if checkCount == 0:
                    for box in Map_Box.boxes:
                        if collideCheck(player, box) == "left" or collideCheck(player, box) == "right":
                            collipse = True
                            break
                elif checkCount == 1:
                    for brick in Map_Brick.bricks:
                        if collideCheck(player, brick) == "left" or collideCheck(player, brick) == "right":
                            collipse = True
                            break
                elif checkCount == 2:
                    for pipe in Map_Pipe.pipes:
                        if collideCheck(player, pipe) == "left" or collideCheck(player, pipe) == "right":
                            collipse = True
                            break
                elif checkCount == 3:
                    for tile in Map_Tile.tiles:
                        if collideCheck(player, tile) == "left" or collideCheck(player, tile) == "right":
                            collipse = True
                            break

                checkCount += 1

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
        checkCount = 0
        # 점프 중 player의 윗부분 충돌
        while (not collipse and checkCount < 4):
            if checkCount == 0:
                for box in Map_Box.boxes:
                    if collideCheck(player, box) == "top":
                        # 충돌한 박스가 충돌하면 아이템이 나오는 question box 인 경우.
                        if not box.isUsed:
                            if box.itemValue == Map_Box.boxType.coin:
                                # 코인(이펙트) 생성
                                newCoin = Item_Coin.Coin()
                                newCoin.x, newCoin.y = box.x, box.y + box.frameY/2 + 15
                                newCoin.isEffect = True
                                Item_Coin.coins.append(newCoin)
                                game_world.add_object(newCoin, 0)

                                game_data.gameData.coin += 1
                            elif box.itemValue == Map_Box.boxType.mushroom:
                                newMush = Item_TransForm.TransformItem()
                                newMush.x, newMush.y = box.x, box.y + box.frameY
                                newMush.itemValue = Item_TransForm.Value.Mushroom
                                Item_TransForm.transItems.append(newMush)
                                game_world.add_object(newMush, 1)
                            elif box.itemValue == Map_Box.boxType.flower:
                                newFlower = Item_TransForm.TransformItem()
                                newFlower.x, newFlower.y = box.x, box.y + box.frameY
                                newFlower.isReverse = False
                                newFlower.itemValue = Item_TransForm.Value.Fireflower
                                Item_TransForm.transItems.append(newFlower)
                                game_world.add_object(newFlower, 1)
                            # Box를 사용한 상태로 변경
                            box.isUsed = True

                        # 충돌 상태 True
                        box.slowFrame = 0
                        box.frame = 0
                        collipse = True
                        break
            elif checkCount == 1:
                for brick in Map_Brick.bricks:
                    if collideCheck(player, brick) == "top":
                        collipse = True
                        break
            elif checkCount == 2:
                for pipe in Map_Pipe.pipes:
                    if collideCheck(player, pipe) == "top":
                        collipse = True
                        break
            elif checkCount == 3:
                for tile in Map_Tile.tiles:
                    if collideCheck(player, tile) == "top":
                        collipse = True
                        break

            checkCount += 1

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
        checkCount = 0

        while (not collipse and checkCount < 4):
            if checkCount == 0:
                for box in Map_Box.boxes:
                    if collideCheck(player, box) == "bottom":
                        player.y = box.y + box.frameY/2 + player.frameY/2
                        collipse = True
                        break
            elif checkCount == 1:
                for brick in Map_Brick.bricks:
                    if collideCheck(player, brick) == "bottom":
                        player.y = brick.y + brick.frameY/2 + player.frameY/2
                        collipse = True
                        break
            elif checkCount == 2:
                for pipe in Map_Pipe.pipes:
                    if collideCheck(player, pipe) == "bottom":
                        player.y = pipe.y + pipe.frameY/2 + player.frameY/2
                        collipse = True
                        break
            elif checkCount == 3:
                for tile in Map_Tile.tiles:
                    if collideCheck(player, tile) == "bottom":
                        player.y = tile.y + tile.frameY/2 + player.frameY/2
                        collipse = True
                        break

            checkCount += 1

        if not collipse:
            #=== 이동
            player.timer_jump += game_framework.frame_time

            # x축 이동
            if player.isMovingInAir:
                # x축 이동
                if player.isMovingInAir:
                    # 충돌 체크 (왼쪽 or 오른쪽이이 오브젝트로 혀있는지 확인)
                    collipse = False
                    checkCount = 0
                    while (not collipse and checkCount < 4):
                        if checkCount == 0:
                            for box in Map_Box.boxes:
                                if collideCheck(player, box) == "left" or collideCheck(player, box) == "right":
                                    collipse = True
                                    break
                        elif checkCount == 1:
                            for brick in Map_Brick.bricks:
                                if collideCheck(player, brick) == "left" or collideCheck(player, brick) == "right":
                                    collipse = True
                                    break
                        elif checkCount == 2:
                            for pipe in Map_Pipe.pipes:
                                if collideCheck(player, pipe) == "left" or collideCheck(player, pipe) == "right":
                                    collipse = True
                                    break
                        elif checkCount == 3:
                            for tile in Map_Tile.tiles:
                                if collideCheck(player, tile) == "left" or collideCheck(player, tile) == "right":
                                    collipse = True
                                    break

                        checkCount += 1

                    # 충돌하지 않았을 때에만 이동
                    if not collipse:
                        player.x += player.velocity * game_framework.frame_time
                        player.x = clamp(25, player.x, 6600 - 25)

            # 낙하 (수직낙하운동)
            # v = v0 + gt, v0 = 0 -> v = gt 에서
            # v = gt --(적분)--> S = 1/2 g t^2 + C (C = S0)  (*Game Design 폴더 참고)
            player.y = (1/2) * GRAVITY_ACCEL_PPS2 * (player.timer_jump ** 2) + player.pos_startFalling

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
        player.timer_jump = clamp(0, player.timer_jump, 0.3)

        player.y += (1/2) * GRAVITY_ACCEL_PPS2 * (player.timer_jump ** 2)

        # print('V = ' + str(vel_jump) + ', yPos = ' + str(player.y) + ', time = ' + str(player.timer_jump))

        collipse = False
        checkCount = 0
        # 충돌해서 착지를 할 때
        while (not collipse and checkCount < 4):
            if checkCount == 0:
                for box in Map_Box.boxes:
                    if collideCheck(player, box) == "bottom":
                        player.y = box.y + box.frameY / 2 + player.frameY / 2
                        collipse = True

                        # 충돌한 박스가 충돌하면 아이템이 나오는 question box 인 경우.
                        if not box.isUsed:
                            if box.itemValue == Map_Box.boxType.coin:
                                # 코인(이펙트) 생성
                                newCoin = Item_Coin.Coin()
                                newCoin.x, newCoin.y = box.x, box.y - box.frameY/2 - 15
                                newCoin.isEffect = True
                                Item_Coin.coins.append(newCoin)
                                game_world.add_object(newCoin, 0)

                                game_data.gameData.coin += 1
                            elif box.itemValue == Map_Box.boxType.mushroom:
                                newMush = Item_TransForm.TransformItem()
                                newMush.x, newMush.y = box.x, box.y - box.frameY
                                newMush.itemValue = Item_TransForm.transitem_Value.Mushroom
                                Item_TransForm.transItems.append(newMush)
                                game_world.add_object(newMush, 1)
                            elif box.itemValue == Map_Box.boxType.flower:
                                newFlower = Item_TransForm.TransformItem()
                                newFlower.x, newFlower.y = box.x, box.y - box.frameY
                                newFlower.isReverse = True
                                newFlower.itemValue = Item_TransForm.transitem_Value.Fireflower
                                Item_TransForm.transItems.append(newFlower)
                                game_world.add_object(newFlower, 1)
                            # Box를 사용한 상태로 변경
                            box.isUsed = True
                        break
            elif checkCount == 1:
                for brick in Map_Brick.bricks:
                    if collideCheck(player, brick) == "bottom":
                        player.y = brick.y + brick.frameY/2 + player.frameY/2  # 발판 위로 올림
                        collipse = True
                        break
            elif checkCount == 2:
                for pipe in Map_Pipe.pipes:
                    if collideCheck(player, pipe) == "bottom":
                        player.y = pipe.y + pipe.frameY/2 + player.frameY/2  # 발판 위로 올림
                        collipse = True
                        break
            elif checkCount == 3:
                for tile in Map_Tile.tiles:
                    if collideCheck(player, tile) == "bottom":
                        player.y = tile.y + tile.frameY/2 + player.frameY/2  # 발판 위로 올림
                        collipse = True
                        break

            checkCount += 1

        if collipse:
            player.add_event(LANDING_EVENT)


    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, player.imageH - player.frameY * P_State.S_Slide,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)


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


    def exit(player, event):
        if event == TRANS2IDLE_EVENT or event == TRANS2RUN_EVENT or event == TRANS2DASH_EVENT:
            player.prevState = None
            player.isTrans = True

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if player.frame >= 5:
            if player.prevState == "RunState":
                player.add_event(TRANS2RUN_EVENT)
            elif player.prevState == "DashState":
                player.add_event(TRANS2DASH_EVENT)
            else:
                player.add_event(TRANS2IDLE_EVENT)


    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, 0, player.frameX, player.frameY
                               , player.x - player.scrollX, player.y)


next_state_table = {
    IdleState: {RIGHT_DOWN: RunState, LEFT_DOWN: RunState, RIGHT_UP: IdleState, LEFT_UP: IdleState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: IdleState, SHIFT_UP: IdleState
        , SPACE: IdleState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState},
    RunState: {RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, LEFT_UP: IdleState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: DashState, SHIFT_UP: RunState
        , SPACE: RunState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState},
    DashState: {RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, LEFT_UP: IdleState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: RunState, SHIFT_UP: RunState
        , SPACE: DashState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState},
    DownState: {RIGHT_DOWN: DownState, LEFT_DOWN: DownState, RIGHT_UP: DownState, LEFT_UP: DownState
        , UP_DOWN: DownState, UP_UP: DownState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: DownState, SHIFT_UP: DownState
        , SPACE: DownState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState},
    JumpState: {RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState, RIGHT_UP: JumpState, LEFT_UP: JumpState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: GroundpoundState, DOWN_UP: JumpState
        , SHIFT_DOWN: JumpState, SHIFT_UP: JumpState
        , SPACE: JumpState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState},
    FallingState: {RIGHT_DOWN: FallingState, LEFT_DOWN: FallingState, RIGHT_UP: FallingState, LEFT_UP: FallingState
        , UP_DOWN: FallingState, UP_UP: FallingState, DOWN_DOWN: GroundpoundState, DOWN_UP: FallingState
        , SHIFT_DOWN: FallingState, SHIFT_UP: FallingState
        , SPACE: FallingState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState},
    GroundpoundState: {RIGHT_DOWN: GroundpoundState, LEFT_DOWN: GroundpoundState, RIGHT_UP: GroundpoundState, LEFT_UP: GroundpoundState
        , UP_DOWN: GroundpoundState, UP_UP: GroundpoundState, DOWN_DOWN: GroundpoundState, DOWN_UP: GroundpoundState
        , SHIFT_DOWN: GroundpoundState, SHIFT_UP: GroundpoundState
        , SPACE: GroundpoundState
        , FALLING_EVENT: FallingState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState
        , TRANSLATE_EVENT: TranslateState},
    TranslateState: {RIGHT_DOWN: TranslateState, LEFT_DOWN: TranslateState, RIGHT_UP: TranslateState, LEFT_UP: TranslateState
        , UP_DOWN: TranslateState, UP_UP: TranslateState, DOWN_DOWN: TranslateState, DOWN_UP: TranslateState
        , SHIFT_DOWN: TranslateState, SHIFT_UP: TranslateState
        , SPACE: TranslateState
        , FALLING_EVENT: TranslateState
        , LANDING_EVENT: TranslateState, LANDING_RUN_EVENT: TranslateState, LANDING_DASH_EVENT: TranslateState
        , TRANSLATE_EVENT: IdleState, TRANS2IDLE_EVENT: IdleState, TRANS2RUN_EVENT: RunState, TRANS2DASH_EVENT: DashState, TRANS2JUMP: JumpState}
}


class Player:
    image_StandardL = None
    def __init__(self):
        # position
        self.x, self.y = 100, 60
        self.frameX, self.frameY = 40, 30
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

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        self.show_bb = False    # 바운딩박스 출력

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

        # 변신 아이템 충돌
        for transItem in Item_TransForm.transItems:
            if not collideCheck(self, transItem) == None:
                if self.transform < transItem.itemValue:
                    self.prevState = self.cur_state.__name__  # 이전상태의 이름을 저장해둔다.
                    if not self.cur_state == JumpState or self.cur_state == GroundpoundState: #버그방지용
                        self.y += 15

                    if transItem.itemValue == Item_TransForm.Value.Mushroom:
                        self.transform = P_Transform.T_Super
                    elif transItem.itemValue == Item_TransForm.Value.Fireflower:
                        self.transform = P_Transform.T_Fire
                    game_data.gameData.transform = self.transform   # 게임데이터 최신화
                    # Frame Image Update
                    self.frameX, self.frameY = 40, 60
                    self.imageH = 660
                    self.add_event(TRANSLATE_EVENT)

                # 해당 충돌 아이템 삭제
                Item_TransForm.transItems.remove(transItem)
                game_world.remove_object(transItem)
                break

        #=== 몬스터
        if self.never_collide_with_mob: # 무적시간
            self.ncwmTimer -= game_framework.frame_time
            if self.ncwmTimer <= 0:
                self.never_collide_with_mob = False
        # goomba
        for goomba in mob_goomba.goombas:
            if not goomba.ismoving:
                # goomba는 화면에 처음 잡혔을 때부터 움직이기 시작한다.
                if self.x <= goomba.x <= self.x + 800:
                    goomba.ismoving = True
            else:
                # goomba의 시야에 플레이어가 들어오면 돌진을 시작한다.
                if goomba.dir == 1:
                    if goomba.x < self.x < goomba.x + 300:
                        goomba.state = mob_goomba.G_State.Dash
                    else:
                        goomba.state = mob_goomba.G_State.Walk
                else:
                    if goomba.x - 300 < self.x < goomba.x:
                        goomba.state = mob_goomba.G_State.Dash
                    else:
                        goomba.state = mob_goomba.G_State.Walk

                # 충돌체크
                if not collideCheck(self, goomba) == None:
                    if self.cur_state == FallingState or self.cur_state == GroundpoundState:
                        if collideCheck(self, goomba) == 'bottom':
                            mob_goomba.goombas.remove(goomba)
                            game_world.remove_object(goomba)
                    else:
                        if not self.never_collide_with_mob:
                            game_data.gameData.life -= 1
                            if not self.never_collide_with_mob:
                                self.never_collide_with_mob = True  # 몹과 충돌하지 않는 상태가 되어서
                                self.ncwmTimer = 1000               # 1초의 무적시간이 주어진다.
                            if self.transform > P_Transform.T_Basic:
                                if self.transform == P_Transform.T_Fire:
                                    self.transform = P_Transform.T_Super
                                elif self.transform == P_Transform.T_Super:
                                    self.transform = P_Transform.T_Basic
                            else:
                                print('Game over')#


    def get_boundingbox(self):  # 바운딩박스
        return self.x - self.frameX/2, self.y + self.frameY/2, self.x + self.frameX/2, self.y - self.frameY/2

    def draw(self):
        self.cur_state.draw(self)

        # bounding box
        if self.show_bb:
            draw_rectangle(self.x - self.frameX/2 - self.scrollX, self.y + self.frameY/2
                           , self.x + self.frameX/2 - self.scrollX, self.y - self.frameY/2)

        # Debug #
        self.font.draw(self.x - 60 - self.scrollX, self.y + 70, 'State' + str(self.cur_state), (255, 255, 0))
        self.font.draw(self.x - 60 - self.scrollX, self.y + 50, 'Dir ' + str(self.dir), (255, 255, 0))
        ###

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

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
            else:
                self.show_bb = True
                Map_Box.show_bb = True
                Map_Brick.show_bb = True
                Map_Pipe.show_bb = True
                Map_Tile.show_bb = True
                Item_TransForm.show_bb = True
                mob_goomba.show_bb = True
                Map_Castle.show_bb = True

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):#test
            score = game_data.gameData.score
            coin = game_data.gameData.coin
            life = game_data.gameData.life
            transform = game_data.gameData.transform
            print('Life: ' + str(life), ' | Score: ' + str(score)
                  + ' | Coin: ' + str(coin) + ' | Transform: ' + str(transform))
