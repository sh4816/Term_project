import game_framework
import enum
import math
from collide import *
from pico2d import *
from ball import Ball

import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe
import Item_Coin
import Item_TransForm

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
JUMP_V0_PPS = 400.0 # px/s
GRAVITY_ACCEL_PPS2 = -400.0 # px/s^2


# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

# State
# 변신 상태
class P_Transform(enum.IntEnum):
    T_Basic = enum.auto()
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
    ,FALLING_EVENT, LANDING_EVENT, LANDING_RUN_EVENT, LANDING_DASH_EVENT = range(15)

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

        if player.dir == 1:
            player.image = load_image('Mario.png')
        else:
            player.image = load_image('MarioL.png')


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

        # 충돌 체크 - 발판

        pass

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, 300, player.frameX, player.frameY
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

        if player.dir == 1:
            player.image = load_image('Mario.png')
        elif player.dir == -1:
            player.image = load_image('MarioL.png')


    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

        if event == RIGHT_DOWN or event == LEFT_DOWN:
            player.isDoubleInput = True

        if event == UP_DOWN:
            player.isMovingInAir = True

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        player.x += player.velocity * game_framework.frame_time

        player.x = clamp(25, player.x, 6600 - 25)

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, 300 - player.frameY * P_State.S_Run,
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
        if player.dir == 1:
            player.image = load_image('Mario.png')
        elif player.dir == -1:
            player.image = load_image('MarioL.png')

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

        if event == SHIFT_UP:
            player.isDash = False

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        player.x += player.velocity * game_framework.frame_time

        player.x = clamp(25, player.x, 6600 - 25)

    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, 300 - player.frameY * P_State.S_Dash,
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
        player.image.clip_draw(int(player.frame) * player.frameX, 300 - player.frameY * P_State.S_Down,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)


class JumpState:
    def enter(player, event):
        player.frame = 0
        player.velocity = 0

        if not player.isJumping:
            player.timer_jump = 0
            player.Variable_V0_PPS = JUMP_V0_PPS
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

        # 이미지
        if player.dir == 1:
            player.image = load_image('Mario.png')
        elif player.dir == -1:
            player.image = load_image('MarioL.png')

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()

        if event == RIGHT_UP or event == LEFT_UP:
            player.isMovingInAir = False

        if event == SHIFT_UP:
            player.isDash = False

    def do(player):
        # 위 아래로 이동
        player.timer_jump += game_framework.frame_time

        vel_jump = JUMP_V0_PPS + GRAVITY_ACCEL_PPS2 * player.timer_jump   # v = v0 + at

        # 위치
        if not player.isCollideJumping:
            # v(속도) = v0 + at --(적분)--> s(위치) = (1/2 at + v)t + s0
            player.y = ((1/2) * GRAVITY_ACCEL_PPS2 * player.timer_jump + JUMP_V0_PPS) * player.timer_jump + player.jump_startY
        else:
            # S = S1 + 1/2 a(t0 - time)^2  (*Game design 폴더 참고)
            player.y = player.pos_collideJumping + (1/2) * GRAVITY_ACCEL_PPS2 * ((player.timer_jump - player.time_collideJumping) ** 2)

        # print('V = ' + str(vel_jump) + ', yPos = ' + str(player.y) + ', time = ' + str(player.timer_jump))

        # 이동
        if player.isMovingInAir:
            player.x += player.velocity * game_framework.frame_time

        # 상태 별 행동
        if not player.isFalling:
            #=== 충돌 체크
            collipse = False
            checkCount = 0
            # 충돌해서 착지를 할 때
            while (not collipse and checkCount < 4):
                if checkCount == 0:
                    for box in Map_Box.boxes:
                        if collideCheck(player, box) == "top":
                            print("'Player top & Box' Collide!")  #
                            collipse = True
                            break
                elif checkCount == 1:
                    for brick in Map_Brick.bricks:
                        if collideCheck(player, brick) == "top":
                            print("'Player top & Brick' Collide!")  #
                            collipse = True
                            break
                elif checkCount == 2:
                    for pipe in Map_Pipe.pipes:
                        if collideCheck(player, pipe) == "top":
                            print("'Player top & Pipe' Collide!")  #
                            collipse = True
                            break
                elif checkCount == 3:
                    for tile in Map_Tile.tiles:
                        if collideCheck(player, tile) == "top":
                            print("'Player top & Tile' Collide!")  #
                            collipse = True
                            break

                checkCount += 1

            if collipse:
                player.isFalling = True

                player.isCollideJumping = True                       # 점프 중에 충돌했는 지 #test
                player.pos_collideJumping = player.y                 # 점프 중에 충돌한 시점의 좌표 #test
                player.time_collideJumping = player.timer_jump       # 점프 중에 충돌한 시점의 시점 #test

                collipse = False

            #===변곡점을 지나면 도약 상태에서 낙하 상태로 변경 (state변경X, bool값만 변경)
            if vel_jump <= 0:
                player.isFalling = True
                print('Fall')

        elif player.isFalling:
            #=== 충돌 체크
            collipse = False
            checkCount = 0
            # 충돌해서 착지를 할 때
            while (not collipse and checkCount < 4):
                if checkCount == 0:
                    for box in Map_Box.boxes:
                        if collideCheck(player, box) == "bottom":
                            print("'Player bottom & Box' Collide!")  #
                            player.y = box.y + box.frameY  # 발판 위로 올림
                            collipse = True
                            break
                elif checkCount == 1:
                    for brick in Map_Brick.bricks:
                        if collideCheck(player, brick) == "bottom":
                            print("'Player bottom & Brick' Collide!")  #
                            player.y = brick.y + brick.frameY  # 발판 위로 올림
                            collipse = True
                            break
                elif checkCount == 2:
                    for pipe in Map_Pipe.pipes:
                        if collideCheck(player, pipe) == "bottom":
                            print("'Player bottom & Pipe' Collide!")  #
                            player.y = pipe.y + pipe.frameY  # 발판 위로 올림
                            collipse = True
                            break
                elif checkCount == 3:
                    for tile in Map_Tile.tiles:
                        if collideCheck(player, tile) == "bottom":
                            print("'Player bottom & Tile' Collide!")  #
                            player.y = tile.y + tile.frameY  # 발판 위로 올림
                            collipse = True
                            break

                checkCount += 1

            if collipse:
                # 초기화
                player.isFalling = False
                player.isJumping = False
                player.timer_jump = 0

                player.isCollideJumping = False  # 점프 중에 충돌했는 지 #test
                player.pos_collideJumping = 0    # 점프 중에 충돌한 시점의 좌표 #test
                player.time_collideJumping = 0   # 점프 중에 충돌한 시점의 시점 #test

                # 다음 상태 지정
                if player.isMovingInAir:
                    if player.isDash:
                        player.add_event(LANDING_DASH_EVENT)
                    else:
                        player.add_event(LANDING_RUN_EVENT)
                else:
                    player.add_event(LANDING_EVENT)
                collipse = False


    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, 300 - player.frameY * P_State.S_Jump,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)


class GroundpoundState:
    def enter(player, event):
        player.frame = 0
        player.velocity = 0

        # 점프에 필요했던 변수들 초기화
        if player.isJumping: player.isJumping = False
        if player.isFalling: player.isFalling = False
        if player.isMovingInAir: player.isMovingInAir = False
        player.timer_jump = 0

        # 기타 변수들 초기화
        if player.isDash: player.isDash = False

        # 속도
        player.velocity = 0

        # 이미지
        if player.dir == 1:
            player.image = load_image('Mario.png')
        elif player.dir == -1:
            player.image = load_image('MarioL.png')

    def exit(player, event):
        pass

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
                        print("'Player bottom & Box' Collide!")  #
                        player.y = box.y + box.frameY  # 발판 위로 올림
                        collipse = True
                        break
            elif checkCount == 1:
                for brick in Map_Brick.bricks:
                    if collideCheck(player, brick) == "bottom":
                        print("'Player bottom & Brick' Collide!")  #
                        player.y = brick.y + brick.frameY  # 발판 위로 올림
                        collipse = True
                        break
            elif checkCount == 2:
                for pipe in Map_Pipe.pipes:
                    if collideCheck(player, pipe) == "bottom":
                        print("'Player bottom & Pipe' Collide!")  #
                        player.y = pipe.y + pipe.frameY  # 발판 위로 올림
                        collipse = True
                        break
            elif checkCount == 3:
                for tile in Map_Tile.tiles:
                    if collideCheck(player, tile) == "bottom":
                        print("'Player bottom & Tile' Collide!")  #
                        player.y = tile.y + tile.frameY  # 발판 위로 올림
                        collipse = True
                        break

            checkCount += 1

        if collipse:
            player.isFalling = False
            player.isJumping = False
            player.timer_jump = 0

            player.add_event(LANDING_EVENT)
            collipse = False


    def draw(player):
        player.image.clip_draw(int(player.frame) * player.frameX, 300 - player.frameY * P_State.S_Slide,
                               player.frameX, player.frameY, player.x - player.scrollX, player.y)

next_state_table = {
    IdleState: {RIGHT_DOWN: RunState, LEFT_DOWN: RunState, RIGHT_UP: IdleState, LEFT_UP: IdleState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: IdleState, SHIFT_UP: IdleState
        , SPACE: IdleState},
    RunState: {RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, LEFT_UP: IdleState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: DashState, SHIFT_UP: RunState
        , SPACE: RunState},
    DashState: {RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, LEFT_UP: IdleState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: RunState, SHIFT_UP: RunState
        , SPACE: DashState},
    DownState: {RIGHT_DOWN: DownState, LEFT_DOWN: DownState, RIGHT_UP: DownState, LEFT_UP: DownState
        , UP_DOWN: DownState, UP_UP: DownState, DOWN_DOWN: DownState, DOWN_UP: IdleState
        , SHIFT_DOWN: DownState, SHIFT_UP: DownState
        , SPACE: DownState},
    JumpState: {RIGHT_DOWN: JumpState, LEFT_DOWN: JumpState, RIGHT_UP: JumpState, LEFT_UP: JumpState
        , UP_DOWN: JumpState, UP_UP: JumpState, DOWN_DOWN: GroundpoundState, DOWN_UP: JumpState
        , SHIFT_DOWN: JumpState, SHIFT_UP: JumpState
        , SPACE: DownState
        , LANDING_EVENT: IdleState, LANDING_RUN_EVENT: RunState, LANDING_DASH_EVENT: DashState},
    GroundpoundState: {RIGHT_DOWN: GroundpoundState, LEFT_DOWN: GroundpoundState, RIGHT_UP: GroundpoundState, LEFT_UP: GroundpoundState
        , UP_DOWN: GroundpoundState, UP_UP: GroundpoundState, DOWN_DOWN: GroundpoundState, DOWN_UP: GroundpoundState
        , SHIFT_DOWN: GroundpoundState, SHIFT_UP: GroundpoundState
        , SPACE: GroundpoundState
        , LANDING_EVENT: IdleState}
}


class Player:

    def __init__(self):
        # position
        self.x, self.y = 100, 60
        self.frameX, self.frameY = 40, 30

        # Scroll
        self.scrollX = 0

        # Boy is only once created, so instance image loading is fine
        self.image = load_image('Mario.png')

        # Debug #
        self.font = load_font('ENCR10B.TTF', 16)
        ###

        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.timer_jump = 0         # 점프 타이머
        self.jump_startY = 0        # 점프를 시작한 y좌표
        self.Variable_V0_PPS = 0    # V0가 변할 때(ex. 점프 중 충돌) V0를 변경시켜주기 위한 변수
        self.isJumping = False      # 점프 중인지
        self.isFalling = False      # 낙하 중인지

        self.isCollideJumping = False     # 점프 중에 충돌했는 지 #test
        self.pos_collideJumping = 0       # 점프 중에 충돌한 시점의 좌표 #test
        self.time_collideJumping = 0      # 점프 중에 충돌한 시점의 시점 #test

        self.isMovingInAir = False  # 공중에서 움직이는지
        self.isDoubleInput = False  # 키입력이 두 개 동시에 되었는지
        self.isDash = False         # 대쉬 중인지

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)


    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir*SHOOT_SPEED_PPS)
        game_world.add_object(ball, 1)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

        # Debug #
        self.font.draw(self.x - 60 - self.scrollX, self.y + 70, 'State' + str(self.cur_state), (255, 255, 0))
        self.font.draw(self.x - 60 - self.scrollX, self.y + 50, 'Dir ' + str(self.dir), (255, 255, 0))
        ###

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

