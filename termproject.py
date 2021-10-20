#2DGP Term-Project
from pico2d import *
import random

# Game object class here
class BG:#BackGround
    def __init__(self): # 생성자
        self.image = load_image('BG.png')

    def draw(self):
        self.image.draw(400, 300)

class Ground:
    def __init__(self):
        self.image = load_image('ground.png')

    def draw(self):
        self.image.draw(self.startXPos, self.startYPos)

    Width, Height = 0, 0
    startXPos, startYPos = 0, 0


class tile:
    def __init__(self):
        self.image = load_image('tile_grass.png')

    def draw(self):
        self.image.draw(self.startXPos, self.startYPos)

    Width, Height = 0, 0
    startXPos, startYPos = 0, 0

class Character:
    def __init__(self):
        self.image = load_image('Mario.png')
        self.frameX, self.frameY = 40, 60       # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 400, 90
        self.frame = 0
        self.condition = 0
        # < Mario Condition >
        # 0: Idle(1), 1: Walk(2), 2: Hit(1), 3: Jump(1), 4: Dash(4)
        # 5: Down(1), 6: Slide/GroundPound(1), 7: Stand(1), 8: Kick(4), 9: Climb(2)
        # 기본
        self.isLeft = False         # 왼쪽을 보고 있는지
        self.isOnGround = 0         # 땅 위에 있는지 (0: 땅 위에 없음, 1 이상: 땅 위에 있음)

        # 걷기 관련 변수
        self.isWalk = False         # 걷는 중인지

        # 점프 관련 변수
        self.jumpHeight = 15
        self.isLeap = False         # 도약 중인지
        self.isFall = False         # 낙하 중인지
        self.move_in_air = False    # 공중에서 좌우로 움직이는 지

        # 대쉬 관련 변수
        self.dash = False           # 대쉬 중인지
        self.dashJump = False       # 대쉬 중 점프를 하였는 지

        # 그라운드파운드 관련 변수
        self.gp = False             # 그라운드파운드 중인지
        self.gp_StartHeight = 0     # 그라운드파운드를 시작한 높이
        self.gp_EndHeight = 0       # 그라운드파운드를 끝낼 높이(도약 할 때 y값 측정)
        gp_gapHeight = 0
        self.gp_accel = 0           # 그라운드파운드 가속도
        self.gp_delay = 0           # 그라운드파운드 후딜레이

    def update(self):
        # Out of Window 체크
        if self.y < 0:
            # Life 업데이트 후 Life감소 추가 예정.
            self.x, self.y = 400, 200
            print('Test가 끝나면 사망처리')

        # 방향 체크
        if self.isLeft: self.image = load_image('MarioL.png')       # 왼쪽을 보고 있는 리소스
        else:           self.image = load_image('Mario.png')        # 오른쪽을 보고 있는 리소스

        # 발판 체크
        if self.condition == 0 or self.condition == 1 or self.condition == 4:
            # 1. 충돌하면 1을 더한다.
            if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 ground1.Width, ground1.Height, ground1.startXPos, ground1.startYPos):
                self.isOnGround += 1
            elif collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 ground2.Width, ground2.Height, ground2.startXPos, ground2.startYPos):
                self.isOnGround += 1
            # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
            if self.isOnGround == 0:
                changeCondition(self, 3)
                self.isLeap = False
                self.isFall = True
                self.isOnGround = 0
            else:
                self.isOnGround = 0

        # 상태 체크
        #=== Idle
        if self.condition == 0:
            pass
        #=== Walk
        elif self.condition == 1:
            self.frame = (self.frame + 1) % 2
            if self.isLeft:
                self.x -= 5
            else:
                self.x += 5

        #=== Hit
        elif self.condition == 2:
            pass
        #=== Jump
        elif self.condition == 3:
            if self.isLeap:
                self.y += self.jumpHeight
                self.jumpHeight -= 1
                if self.jumpHeight <= 0:
                    self.isLeap = False
                    self.isFall = True
                    self.jumpHeight = 0
            elif self.isFall:
                self.y -= self.jumpHeight
                self.jumpHeight += 1

                # 충돌체크
                # 1. 충돌하면 1을 더한다.
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 ground1.Width, ground1.Height, ground1.startXPos, ground1.startYPos):
                    self.isOnGround += 1
                    self.gp_EndHeight = ground1.startYPos + ground1.Height + 10
                elif collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                   ground2.Width, ground2.Height, ground2.startXPos, ground2.startYPos):
                    self.isOnGround += 110
                    self.gp_EndHeight = ground2.startYPos + ground2.Height + 10
                # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
                if self.isOnGround == 0:
                    self.isOnGround = 0
                else:
                    self.isFall = False
                    self.dashJump = False
                    if self.move_in_air: changeCondition(self, 1)      # walk
                    else:                changeCondition(self, 0)      # idle
                    self.jumpHeight = 15
                    self.isOnGround = 0

                    self.y = self.gp_EndHeight

            # 공중에서 좌우로 움직이는 거
            if self.move_in_air:
                if self.isLeft:
                    if self.dashJump: self.x -= 10
                    else:             self.x -= 5
                else:
                    if self.dashJump: self.x += 10
                    else:             self.x += 5
        #=== Dash
        elif self.condition == 4:
            self.frame = (self.frame + 1) % 4
            if self.isLeft:
                self.x -= 10
            else:
                self.x += 10
        #=== Down
        elif self.condition == 5:
            pass
        #=== GroundPound
        elif self.condition == 6:
            gp_gapHeight = self.gp_StartHeight - self.gp_EndHeight
            self.gp_accel += 1
            # if self.gp_accel >= 10: self.gp_accel -= 1 # 최대 가속도 제한

            # 충돌체크 ( 이동 예정인 좌표와 오브젝트, 현재 좌표X )
            # 1. 충돌하면 1을 더한다.
            if collipseCheck(self.frameX, self.frameY, self.x, self.y - gp_gapHeight / 10 * self.gp_accel,
                             ground1.Width, ground1.Height, ground1.startXPos, ground1.startYPos):
                self.isOnGround += 1
                self.gp_EndHeight = ground1.startYPos + ground1.Height + 10
            elif collipseCheck(self.frameX, self.frameY, self.x, self.y - gp_gapHeight / 10 * self.gp_accel,
                               ground2.Width, ground2.Height, ground2.startXPos, ground2.startYPos):
                self.isOnGround += 1
                self.gp_EndHeight = ground2.startYPos + ground2.Height + 10
            # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
            if self.isOnGround == 0:
                if self.y - (gp_gapHeight / 10 * self.gp_accel): self.gp_delay = 3  # 그라운드파운드 후딜레이 3
                self.y -= gp_gapHeight / 10 * self.gp_accel
            else:
                self.y = self.gp_EndHeight

                # 착지 후 딜레이 계산
                self.gp_delay -= 1
                if (self.gp_delay == 0):
                    changeCondition(self, 0)
                    self.gp = False
                    self.isLeap = False
                    self.isFall = False
                    self.gp_delay = 5
                    gp_gapHeight = 0
                    self.gp_accel = 0

    def draw(self):
        self.image.clip_draw(self.frame*self.frameX, (9-self.condition)*self.frameY
                             , self.frameX, self.frameY, self.x, self.y)


def changeCondition(target, num):  # 상태 바꾸는 함수
    target.condition = num
    target.frame = 0
    target.jumpHeight = 15

def collipseCheck(obj1_w, obj1_h, obj1_cx, obj1_cy, obj2_w, obj2_h, obj2_cx, obj2_cy):  # 충돌 체크 함수
    # 두 사각형의 상하좌우 변
    r1_L, r1_R = obj1_cx - obj1_w/2, obj1_cx + obj1_w/2
    r1_T, r1_B = obj1_cy + obj1_h/2, obj1_cy - obj1_h/2
    r2_L, r2_R = obj2_cx - obj2_w/2, obj2_cx + obj2_w/2
    r2_T, r2_B = obj2_cy + obj2_h/2, obj2_cy - obj2_h/2

    if r1_R > r2_L:                                     # r1의 오른쪽 변이 r2의 왼쪽 변보다 오른쪽에 있을 때
        if not r1_L > r2_R:                             # 단, r1의 왼쪽 변이 r2 보다 오른쪽에 있으면 안된다.
            if r1_B > r2_B and r1_B < r2_T:             # r1의 아랫변이 r2 안에 있는 경우
                return True
            elif r1_T > r2_B and r1_T < r2_T:           # r1의 윗변이 r2 안에 있는 경우
                return True
            elif r1_L > r2_L and r1_L < r2_R:           # r1의 왼쪽 변이 r2 안에 있는 경우
                if not (r1_B > r2_T or r1_T < r2_B):   # 단, r1의 아랫변이 r2 위에 있거나, r1의 윗변이 r2 아래에 있으면 안된다.
                    return True
            elif r1_T > r2_B and r1_B < r2_T:           # r1의 윗변은 r2의 아랫변보다 위에, r1의 아랫변은 r2의 윗변보다 아래에 있는 경우
                if not (r1_L > r2_R or r1_R < r2_L):   # 단, r1의 왼쪽 변이 r2 오른쪽에 있거나, r1의 오른 변이 r2 왼쪽에 있으면 안된다.
                    return True

    if r1_L <= r2_R:                                    # r1의 왼쪽 변이 r2의 오른쪽 변보다 왼쪽에 있을 때
        if not r1_R < r2_L:                             # 단, r1의 오른쪽 변이 r2 보다 왼쪽에 있으면 안된다.
            if r1_B > r2_B and r1_B < r2_T:             # r1의 아랫변이 r2 안에 있는 경우
                return True
            elif r1_T > r2_B and r1_T < r2_T:           # r1의 윗변이 r2 안에 있는 경우
                return True
            elif r1_R > r2_L and r1_R < r2_R:           # r1의 오른쪽 변이 r2 안에 있는 경우
                if not (r1_B > r2_T or r1_T < r2_B):  # 단, r1의 아랫변이 r2 위에 있거나, r1의 윗변이 r2 아래에 있으면 안된다.
                    return True
            elif r1_T > r2_B and r1_B < r2_T:           # r1의 윗변은 r2의 아랫변보다 위에, r1의 아랫변은 r2의 윗변보다 아래에 있는 경우
                if not (r1_L > r2_R or r1_R < r2_L):  # 단, r1의 왼쪽 변이 r2 오른쪽에 있거나, r1의 오른 변이 r2 왼쪽에 있으면 안된다.
                    return True

    if (r1_L > r2_L and r1_L < r2_R) and (r1_R > r2_L and r1_R < r2_R): # r1의 왼쪽, 오른쪽 변 모두 r2 안에 있는 경우
        if not (r1_B > r2_T or r1_T < r2_B):  # 단, r1의 아랫변이 r2 위에 있거나, r1의 윗변이 r2 아래에 있으면 안된다.
            return True

    if (r1_T > r2_B and r1_T < r2_T) and (r1_B > r2_B and r1_B < r2_T): # r1의 윗변, 아랫변 모두 r2 안에 있는 경우
        if not (r1_L > r2_R or r1_R < r2_L):  # 단, r1의 왼쪽 변이 r2 오른쪽에 있거나, r1의 오른 변이 r2 왼쪽에 있으면 안된다.
            return True

    return False    # 위의 모든 경우에 해당하지 않는 경우 False 반환

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:          # 나가기
            running = False                 # 종료
        elif event.type == SDL_KEYDOWN:                         # 키보드 입력
            if event.key == SDLK_ESCAPE:                        # 종료
                running = False
            #=== 좌우 이동
            elif event.key == SDLK_LEFT:                              # 왼쪽 이동
                if not mario.isLeft: mario.isLeft = True              # 왼쪽을 보고 있지 않았다면 왼쪽을 보게 만든다.

                if mario.condition == 0:
                    changeCondition(mario, 1)                         # idle 상태에서만 상태 변경
                    mario.isWalk = True

                if mario.isLeap or mario.isFall:                      # 도약 or 낙하 중
                    mario.move_in_air = True                          # 공중에서 좌우 움직임
            elif event.key == SDLK_RIGHT:                             # 오른쪽 이동
                if mario.isLeft: mario.isLeft = False                 # 왼쪽을 보고 있었다면 오른쪽을 보게 만든다.

                if mario.condition == 0:
                    changeCondition(mario, 1)                         # idle 상태에서만 상태 변경
                    mario.isWalk = True

                if mario.isLeap or mario.isFall:                      # 도약 or 낙하 중
                    mario.move_in_air = True                          # 공중에서 좌우 움직임
            #=== 점프
            elif event.key == SDLK_z:
                if mario.condition == 0 or mario.condition == 1 or mario.condition == 4:
                    if mario.condition == 4:
                        mario.dashJump = True

                    changeCondition(mario, 3)
                    mario.isWalk = False
                    mario.isLeap = True
            #=== 대쉬
            elif event.key == SDLK_x:
                if mario.condition != 3 and mario.isWalk:        # 점프 중에는 대쉬 불가 / 걷는 중에만 대쉬 가능
                    changeCondition(mario, 4)
                    mario.dash = True
            # === 웅크리기 & 그라운드파운드
            elif event.key == SDLK_DOWN:
                # 웅크리기
                if mario.condition == 0 or mario.condition == 1 or mario.condition == 4:
                    if not mario.condition == 5:
                        changeCondition(mario, 5)

                # 그라운드파운드
                if mario.isLeap or mario.isFall:
                    if not mario.condition == 6:
                        changeCondition(mario, 6)
                        mario.gp = True
                        mario.gp_StartHeight = mario.y

        elif event.type == SDL_KEYUP:                                 # 키보드 입력 중지
            # 좌or우 방향키 떼기
            if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:
                if mario.condition == 1:
                    changeCondition(mario, 0)                         # Idle로 전환
                    mario.isWalk = False
                elif mario.condition == 3:
                    if mario.move_in_air: mario.move_in_air = False
                elif mario.condition == 4:
                    mario.dash = False
                    mario.dashJump = False
                    changeCondition(mario, 0)  # Idle로 전환

            # x 키 떼기
            elif event.key == SDLK_x:
                if mario.isLeap or mario.isFall:
                    pass
                elif mario.dash:
                    if mario.isWalk:
                        changeCondition(mario, 1)
                else:
                    changeCondition(mario, 0)                         # walk

                if mario.dash: mario.dash = False                     # 대쉬 중지
            # 아래 방향키 떼기
            elif event.key == SDLK_DOWN:
                if mario.condition == 5:
                    changeCondition(mario, 0)
                    print('Up')  # test


# initialization code
open_canvas()

background = BG()  # 백그라운드 객체를 생성

mario = Character() # 마리오 객체를 생성

#=== 지형
# 타일
# tile_grass

# 일반 땅
ground1 = Ground() # 땅1
ground1.Width, ground1.Height = 300, 30
ground1.startXPos, ground1.startYPos = 300, 50

ground2 = Ground() # 땅2
ground2.Width, ground2.Height = 300, 30
ground2.startXPos, ground2.startYPos = 600, 130


# 무한반복
running = True

# game main loop code
while running:

    handle_events() # 키 입력 받아들이는 처리

    # Game logic
    mario.update()

    # Game drawing
    clear_canvas()
    background.draw()
    mario.draw()
    ground1.draw()
    ground2.draw()

    update_canvas()

    delay(0.05)


# finalization code