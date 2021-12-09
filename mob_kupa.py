from pico2d import *
import enum
import random

import Map_Bridge
import game_framework
import game_world
import mob_kupa_breath
from collide import collideCheck
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe

# Physics Variables...
#
# 마리오의 키는 2M, 몸무게는 70kg 이라 가정,
PIXEL_PER_METER = (30.0 / 1.0)  # 30 pixel == 1m

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

# Kupa Run Speed
def KMPH2MPS(KMPH): # km/h -> m/sec
    MPM = KMPH * 1000.0 / 60.0
    MPS = MPM / 60.0
    return MPS      #return m/sec

MOVE_SPEED_PPS = (KMPH2MPS(8) * PIXEL_PER_METER)
DASH_SPPED_PPS = (KMPH2MPS(15) * PIXEL_PER_METER)
HIDE_SPEED_PPS = (KMPH2MPS(60) * PIXEL_PER_METER)
GRAVITY_ACCEL_PPS2 = -(KMPH2MPS(9) * PIXEL_PER_METER)


# enum
class K_State(enum.IntEnum):
    S_Idle = 0
    S_Walk = enum.auto()
    S_Dash = enum.auto()
    S_Jump = enum.auto()
    S_Fall = enum.auto()
    S_Hit = enum.auto()
    S_Breath = enum.auto()
    S_Hide = enum.auto()

class KupaBB():
    def __init__(self):  # 생성자
        self.frameX, self.frameY = 0, 0
        self.x, self.y = 0, 0
        self.scrollX = 0
kupa_bb = KupaBB()

show_bb = False

class Kupa():
    image = None
    imageL = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 60, 120  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.frame = 0
        self.state = K_State.S_Idle

        self.life = 1

        self.ismoving = False   # 쿠파는 화면에 처음으로 잡혔을 때부터 움직이기 시작한다.
        self.dir = -1
        self.timerFall = 0

        # 브레스 관련
        self.breath_cooldown = False
        self.breath_timer = 0
        self.isFired = True

        # 피격 관련
        self.hit_timer = 0

        # 등껍질 관련
        self.hide_timer = 0

        # 충돌 관련
        self.isOnGround = 0
        self.landYPos = 0

        # 이미지
        if self.image == None:
            self.image = load_image('kupa.png')
            self.imageL = load_image('kupaL.png')

    def update(self):
        # === Bounding Box
        global kupa_bb

        if self.state == K_State.S_Idle or self.state == K_State.S_Walk or self.state == K_State.S_Dash\
                or self.state == K_State.S_Breath or self.state == K_State.S_Jump\
                or self.state == K_State.S_Fall or self.state == K_State.S_Hit:
            kupa_bb.x, kupa_bb.y = self.x, self.y - 20
            kupa_bb.frameX, kupa_bb.frameY = 60, 80
        elif self.state == K_State.S_Hide:
            kupa_bb.x, kupa_bb.y = self.x, self.y - 45
            kupa_bb.frameX, kupa_bb.frameY = 60, 30

        # === Frame
        frameCut = 0
        if self.state == K_State.S_Idle or self.state == K_State.S_Jump or self.state == K_State.S_Fall or self.state == K_State.S_Hit:
            frameCut = 1
        elif self.state == K_State.S_Hide:
            frameCut = 3
        elif self.state == K_State.S_Walk or self.state == K_State.S_Dash or self.state == K_State.S_Breath:
            frameCut = 4

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % frameCut

        # === 바닥에 아무것도 없으면(허공에 있으면) 아래로 낙하
        collipse = False
        for obj in game_world.all_objects():
            if obj.__class__ == Map_Box.Box_Question \
                    or obj.__class__ == Map_Brick.Brick \
                    or obj.__class__ == Map_Pipe.Pipe \
                    or obj.__class__ == Map_Tile.Tile \
                    or obj.__class__ == Map_Bridge.BridgeBoom:  # 충돌체크를 해야할 클래스의 이름
                if collideCheck(self, obj) == "bottom":
                    self.y = obj.y + obj.frameY / 2 + self.frameY / 2
                    collipse = True
                    break

        if not collipse:
            self.timerFall += game_framework.frame_time
            self.y += GRAVITY_ACCEL_PPS2 * (self.timerFall ** 2)  # v = v0 + gt, d = v * t
        else:
            if not self.timerFall == 0:
                self.timerFall = 0

        if self.y < 0 or self.x < 0:
            game_world.remove_object(self)

        # === State: 걷기 또는 대쉬
        if self.state == K_State.S_Walk or self.state == K_State.S_Dash:
            if self.ismoving:
                # === 왼쪽 오른쪽으로 이동
                # 충돌 체크 (왼쪽 or 오른쪽이이 오브젝트로 혀있는지 확인)
                collipse = False
                for obj in game_world.all_objects():
                    if obj.__class__ == Map_Box.Box_Question \
                            or obj.__class__ == Map_Brick.Brick \
                            or obj.__class__ == Map_Pipe.Pipe \
                            or obj.__class__ == Map_Tile.Tile\
                            or obj.__class__ == Map_Bridge.BridgeBoom:  # 충돌체크를 해야할 클래스의 이름
                        if collideCheck(self, obj) == "left":
                            collipse = True
                            self.x = obj.x + obj.frameX/2 + self.frameX/2 + 1
                            break
                        elif collideCheck(self, obj) == "right":
                            collipse = True
                            self.x = obj.x - obj.frameX/2 - self.frameX/2 - 1
                            break

                # 충돌하지 않았을 때에만 이동
                if not collipse:
                    # 움직임
                    if self.state == K_State.S_Walk:
                        self.x += self.dir * MOVE_SPEED_PPS * game_framework.frame_time
                    elif self.state == K_State.S_Dash:
                        self.x += self.dir * DASH_SPPED_PPS * game_framework.frame_time

        # === State: 피격 상태
        elif self.state == K_State.S_Hit:
            self.hit_timer += game_framework.frame_time

            if self.hit_timer >= 3:
                print('피격 무적 해제')
                self.hit_timer = 0
                self.state = K_State.S_Hide

        elif self.state == K_State.S_Breath:
            if not self.isFired:
                self.frame = 0
                self.state = K_State.S_Breath
                rndDir = random.randint(0, 4)
                if rndDir == 3:
                    for i in range(3):
                        mob_kupa_breath.makeFires(self.x, self.y, self.dir, i)
                elif rndDir == 4:
                    mob_kupa_breath.makeFires(self.x, self.y, self.dir, rndDir-1)
                else:
                    mob_kupa_breath.makeFires(self.x, self.y, self.dir, rndDir)
                self.isFired = True

            self.breath_timer += game_framework.frame_time
            if self.breath_timer >= 0.6:
                self.breath_timer = 0
                self.breath_cooldown = True
                self.frame = 0
                self.state = K_State.S_Walk

        elif self.state == K_State.S_Hide:
            self.hide_timer += game_framework.frame_time
            self.x += self.dir * HIDE_SPEED_PPS * game_framework.frame_time

            if self.hide_timer >= 5:
                self.hide_timer = 0
                self.state = K_State.S_Walk

            # 방향전환
            if self.x - self.frameX / 2 <= 0:
                self.dir = 1
                self.x = self.frameX/2
            elif self.x + self.frameX / 2 >= 800:
                self.dir = -1
                self.x = 800 - self.frameX/2


        # === 불덩이 발사 공격
        if self.breath_cooldown:
            self.breath_timer += game_framework.frame_time

            if self.breath_timer >= 1:
                self.breath_timer = 0
                self.isFired = False
                self.breath_cooldown = False


    def draw(self):
        # 렌더링
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * self.frameX, 840 - int(self.state) * self.frameY, self.frameX, self.frameY
                                 , self.x - self.scrollX, self.y)
        else:
            self.imageL.clip_draw(int(self.frame) * self.frameX, 840 - int(self.state) * self.frameY, self.frameX, self.frameY
                                 , self.x - self.scrollX, self.y)

        # bounding box
        global show_bb, kupa_bb
        if show_bb:
            draw_rectangle(kupa_bb.x - kupa_bb.frameX / 2 - kupa_bb.scrollX, kupa_bb.y + kupa_bb.frameY / 2
                           , kupa_bb.x + kupa_bb.frameX / 2 - kupa_bb.scrollX, kupa_bb.y - kupa_bb.frameY / 2)


def makeKupa(xPos, yPos, dir):
    newmob = Kupa()
    newmob.x, newmob.y = xPos, yPos
    newmob.dir = dir

    game_world.add_object(newmob, 1)
