# 2DGP Term-Project
from pico2d import *
import random
from enum import *
from State import *


#=== Game Object
#
#BackGround
class BG:
    def __init__(self): # 생성자
        self.image = load_image('BG.png')

    def draw(self):
        self.image.draw(400, 300)

# 상태창
class StatBar:
    def __init__(self): # 생성자
        self.image = load_image('status.png')
        self.w, self.h = 380, 50 # 이미지 크기가 바뀌면 수정
        self.x, self.y = 800 - 10 - self.w / 2, 600 - 10 - self.h / 2

    def draw(self):
        self.image.draw(self.x, self.y)

# 지형
class Tile:
    def __init__(self):  # 생성자
        self.image = load_image('tile_grass.png')
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.type = "Grass"

    def draw(self):
        if self.type == "Grass":
            self.image = load_image('tile_grass.png')
        elif self.type == "SnowField":
            self.image = load_image('tile_snowfield.png')
        elif self.type == "Dirt":
            self.image = load_image('tile_dirt.png')

        self.image.draw(self.x, self.y)



# 랜덤박스, 부숴지는 박스 등등..
class Box_Question():
    def __init__(self):  # 생성자
        self.image = load_image('block_question.png')
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.frame = 0
        self.slowFrame = 0
        self.itemValue = 0                 # 충돌하면 튀어나오는 아이템 종류 (0: 코인, 1: 버섯, 2: 파이어플라워)

        # 충돌 관련
        self.isCollipse = False
        self.isUsed = False
        self.CollipseDir = 0 # 1: 위 2: 아래

    def update(self):
        if self.isUsed: self.image = load_image('block_used.png')
        else:
            self.image = load_image('block_question.png')

            # 충돌체크 ( 이동 예정인 좌표와 오브젝트, 현재 좌표X )
            # 1. 충돌하면 1을 더한다.
            if collipseCheck(mario.frameX, mario.frameY, mario.x, mario.y + 1,
                             self.frameX, self.frameY, self.x, self.y, True):
                if mario.status == c_state.S_Jump and mario.y < self.y:    # 마리오가 블록 아래에서 점프 중
                    self.isCollipse += 1
                    self.CollipseDir = 2
                elif mario.status == c_state.S_GP and mario.y > self.y:  # 마리오가 그라운드 파운드로 위에서 아래로 찍음
                    self.isCollipse += 1
                    self.CollipseDir = 1
            # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
            if self.isCollipse == 0:
                pass
            else:
                self.isCollipse = 0

                self.frame = 0
                self.slowFrame = 0
                self.isUsed = True

                # 아이템 렌더링 시작
                dropItemPosX, dropItemPosY = self.x, 0
                if self.CollipseDir == 1:
                    dropItemPosY = self.y - self.frameY / 2 - fireflower1.frameY / 2
                elif self.CollipseDir == 2:
                    dropItemPosY = self.y + self.frameY / 2 + fireflower1.frameY / 2


                if self.itemValue == 0:
                    coin1.x, coin1.y = dropItemPosX, dropItemPosY + 5
                    coin1.image = load_image('coin.png')
                    coin1.isRendered = True
                    coin1.isEffect = True

                if self.itemValue == 2:
                    fireflower1.x, fireflower1.y = dropItemPosX, dropItemPosY
                    if self.CollipseDir == 1:
                        fireflower1.image = load_image('item_fireflowerR.png')
                    elif self.CollipseDir == 2:
                        fireflower1.image = load_image('item_fireflower.png')
                    fireflower1.isRendered = True

    def draw(self):
        if self.isUsed:
            self.image.clip_draw(self.frame * self.frameX, 0, self.frameX, self.frameY, self.x, self.y)
        else:
            self.slowFrame += 1
            self.frame = (self.slowFrame // 5) % 4
            self.image.clip_draw(self.frame * self.frameX, 0, self.frameX, self.frameY, self.x, self.y)

class Brick():
    def __init__(self):  # 생성자
        self.image = load_image('block_brick.png')
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0

        # 충돌 관련
        self.isCollipse = False
        self.destroy = 0

    def update(self):
        # 충돌체크
        # 1. 충돌하면 1을 더한다.
        if collipseCheck(mario.frameX, mario.frameY, mario.x, mario.y + 1,
                         self.frameX, self.frameY, self.x, self.y, True):
            if mario.status == c_state.S_Jump and mario.y < self.y:  # 마리오가 블록 아래에서 점프 중
                self.destroy += 1
                self.isCollipse += 1
            elif mario.status == c_state.S_GP and mario.y > self.y:  # 마리오가 그라운드 파운드로 위에서 아래로 찍음
                self.destroy += 1
                self.isCollipse += 1
        # 2. 하나라도 충돌했다면 0이 아니게 됨
        if not self.isCollipse == 0:
            if not self.destroy == 0:
                bricks.remove(self)

    def draw(self):
        self.image.draw(self.x, self.y)

class Fireflower():
    def __init__(self):  # 생성자
        self.image = load_image('item_fireflower.png')
        self.frameX, self.frameY = 15, 15  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0

        self.isRendered = False

        # 충돌 관련
        self.isCollipse = False
        self.isUsed = False

    def update(self):
        if self.isRendered and not self.isUsed:
            # 충돌체크
            # 1. 충돌하면 1을 더한다.
            if collipseCheck(mario.frameX, mario.frameY, mario.x, mario.y,
                             self.frameX, self.frameY, self.x, self.y, True):
                    self.isCollipse += 1
            # 2. 하나라도 충돌했다면 isCollipse는 0이 아니게 된다는 점 이용
            if self.isCollipse == 0:
                pass
            else:
                mario.transform = 2
                mario.status = c_state.S_Transform
                mario.frame = 0
                mario.slowFrame = 0
                self.isCollipse = 0
                self.isUsed = True

    def draw(self):
        if self.isRendered and not self.isUsed:
            self.image.draw(self.x, self.y)

class Fire():
    def __init__(self):  # 생성자
        self.image = load_image('fireball.png')
        self.frameX, self.frameY = 10, 10  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.frame = 0
        self.slowFrame = 0
        self.x, self.y = 0, 0
        self.dir = 0                       # 0: Left 1: Right

        self.isRendered = False

    def draw(self):
        if self.isRendered and self.slowFrame <= 20:
            if self.dir == 0: self.x -= 1
            else:             self.x += 1
            self.slowFrame += 1
            self.frame = (self.slowFrame // 2) % 4
            self.image.clip_draw(self.frame * self.frameX, 0, self.frameX, self.frameY, self.x, self.y)
        else:
            # self.x, self.y = -999, -999
            self.isRendered = False

class Coin():
    def __init__(self):  # 생성자
        self.image = load_image('coin.png')
        self.frameX, self.frameY = 20, 20  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.frame = 0
        self.slowFrame = 0
        self.x, self.y = 0, 0

        self.isRendered = False
        self.isEffect = False

        # 충돌 관련
        self.isCollipse = False
        self.isUsed = False

    def update(self):
        pass

    def draw(self):
        if self.isRendered and not self.isUsed:
            self.slowFrame += 1
            self.frame = (self.slowFrame // 4) % 4
            self.image.clip_draw(self.frame * self.frameX, 0, self.frameX, self.frameY, self.x, self.y)

            if self.isEffect:
                if self.slowFrame >= 16:
                    self.isRendered = False
        else:
            self.slowFrame = 0
            self.frame = 0
            self.isRendered = False
            self.isEffect = False
            self.isCollipse = False
            self.isUsed = False

#=== Function
#

# 충돌 체크 함수
def get_box():

    return

def collipseCheck(obj1_w, obj1_h, obj1_cx, obj1_cy, obj2_w, obj2_h, obj2_cx, obj2_cy, isPlayer):
    # 두 사각형의 상하좌우 변
    r1_L, r1_R = obj1_cx - obj1_w/2, obj1_cx + obj1_w/2
    r1_T, r1_B = obj1_cy + obj1_h/2, obj1_cy - obj1_h/2
    r2_L, r2_R = obj2_cx - obj2_w/2, obj2_cx + obj2_w/2
    r2_T, r2_B = obj2_cy + obj2_h/2, obj2_cy - obj2_h/2

    if isPlayer:    # Player의 리소스 파일 크기때문에 플레이어 발 아래에 발판이 없는 것 처럼 보이지만, 충돌처리가 되는 경우 방지.
        if mario.isLeft:
            r1_L += 15
            r1_R -= 12
        else:
            r1_L += 12
            r1_R -= 15

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


#=== Handle Events
#
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
                if mario.status == c_state.S_Idle:
                    mario.status = c_state.S_Walk
                    mario.isWalk = True
                    mario.frame = 0
                    mario.slowFrame = 0
                elif mario.status == c_state.S_Walk:
                    if mario.isWalk and not mario.isLeft:
                        mario.status = c_state.S_Idle
                        mario.isWalk = False
                        mario.frame = 0
                        mario.slowFrame = 0

                        mario.doubleInput = True

                if mario.isLeap or mario.isFall:                      # 도약 or 낙하 중
                    mario.move_in_air = True                          # 공중에서 좌우 움직임

                if not mario.isLeft: mario.isLeft = True  # 왼쪽을 보고 있지 않았다면 왼쪽을 보게 만든다.

            elif event.key == SDLK_RIGHT:                             # 오른쪽 이동
                if mario.status == c_state.S_Idle:
                    mario.status = c_state.S_Walk
                    mario.isWalk = True
                    mario.frame = 0
                    mario.slowFrame = 0
                elif mario.status == c_state.S_Walk:
                    if mario.isWalk and mario.isLeft:
                            mario.status = c_state.S_Idle
                            mario.isWalk = False
                            mario.frame = 0
                            mario.slowFrame = 0

                            mario.doubleInput = True

                if mario.isLeap or mario.isFall:                      # 도약 or 낙하 중
                    mario.move_in_air = True                          # 공중에서 좌우 움직임

                if mario.isLeft: mario.isLeft = False  # 왼쪽을 보고 있었다면 오른쪽을 보게 만든다.

            #=== z - 점프
            elif event.key == SDLK_z:
                if mario.status == c_state.S_Idle:
                    mario.status = c_state.S_Jump
                    mario.isLeap = True
                    mario.isWalk = False
                    mario.move_in_air = False
                    mario.dash = False
                    mario.dashJump = False
                    mario.frame = 0
                    mario.slowFrame = 0
                elif mario.status == c_state.S_Walk:
                    mario.status = c_state.S_Jump
                    mario.isLeap = True
                    mario.isWalk = False
                    mario.move_in_air = True
                    mario.dash = False
                    mario.dashJump = False
                    mario.frame = 0
                    mario.slowFrame = 0
                elif mario.status == c_state.S_Dash:
                    mario.status = c_state.S_Jump
                    mario.isLeap = True
                    mario.isWalk = False
                    mario.move_in_air = True
                    mario.dash = False
                    mario.dashJump = True
                    mario.frame = 0
                    mario.slowFrame = 0
            #=== x - 대쉬
            elif event.key == SDLK_x:
                if mario.status != c_state.S_Jump and mario.isWalk:        # 점프 중에는 대쉬 불가 / 걷는 중에만 대쉬 가능
                    mario.status = c_state.S_Dash
                    mario.frame = 0
                    mario.slowFrame = 0

                    mario.dash = True
            # === 아래 - 웅크리기 & 그라운드파운드
            elif event.key == SDLK_DOWN:
                # 웅크리기
                if mario.status == c_state.S_Idle or mario.status == c_state.S_Walk or mario.status == c_state.S_Dash:
                    if not mario.status == c_state.S_Down:
                        mario.status = c_state.S_Down
                        mario.frame = 0
                        mario.slowFrame = 0


                # 그라운드파운드
                if mario.isLeap or mario.isFall:
                    if not mario.status == c_state.S_GP:
                        mario.status = c_state.S_GP
                        mario.frame = 0
                        mario.slowFrame = 0

                        mario.gp = True
                        mario.gp_StartHeight = mario.y
            #=== c - 액션/공격
            elif event.key == SDLK_c:
                if mario.transform == 2:
                    if mario.status == c_state.S_Idle or mario.status == c_state.S_Walk:
                        mario.status = c_state.S_Action
                        mario.frame = 0
                        mario.slowFrame = 0

                        mario.act = True
                        mario.act_Delay = 4
            #=== t - "테스트 전용" 좌표값 출력
            elif event.key == SDLK_t:
                print('Pos: ' + str((mario.x, mario.y)) + ', Status: ' + str(mario.status))
                if mario.isWalk: print('IsWalk: O')
                if mario.dash: print('IsDash: O')
                if mario.isLeap: print('IsLeap: O')
                if mario.isFall: print('IsFall: O')
        # 키보드 입력 중지
        elif event.type == SDL_KEYUP:
            # 좌 방향키 떼기
            if event.key == SDLK_LEFT:
                if mario.status == c_state.S_Idle and mario.doubleInput:
                        mario.status = c_state.S_Walk
                        mario.isWalk = True
                        mario.frame = 0
                        mario.slowFrame = 0
                        mario.isLeft = False
                elif mario.status == c_state.S_Walk and mario.isLeft:
                    mario.status = c_state.S_Idle
                    mario.isWalk = False
                    mario.frame = 0
                    mario.slowFrame = 0

                    mario.isWalk = False
                elif mario.status == c_state.S_Jump:
                    mario.move_in_air = False
                    mario.isWalk = False
                elif mario.status == c_state.S_Dash:
                    mario.status = c_state.S_Idle
                    mario.dash = False
                    mario.dashJump = False
                    mario.isWalk = False
                    mario.frame = 0
                    mario.slowFrame = 0


            # 우 방향키 떼기
            elif event.key == SDLK_RIGHT:
                if mario.status == c_state.S_Idle and mario.doubleInput:
                        mario.status = c_state.S_Walk
                        mario.isWalk = True
                        mario.frame = 0
                        mario.slowFrame = 0
                        mario.isLeft = True
                elif mario.status == c_state.S_Walk:
                    mario.status = c_state.S_Idle
                    mario.isWalk = False
                    mario.frame = 0
                    mario.slowFrame = 0

                    mario.isWalk = False
                elif mario.status == c_state.S_Jump:
                    mario.move_in_air = False
                    mario.isWalk = False
                elif mario.status == c_state.S_Dash:
                    mario.status = c_state.S_Idle
                    mario.dash = False
                    mario.dashJump = False
                    mario.isWalk = False
                    mario.frame = 0
                    mario.slowFrame = 0


            # x 키 떼기
            elif event.key == SDLK_x:
                if mario.dash and mario.isWalk:
                    mario.status = c_state.S_Walk
                    mario.dash = False
                    mario.frame = 0
                    mario.slowFrame = 0

                # else:
                #     mario.status = c_state.S_Idle
                #     mario.dash = False
                #     mario.isWalk = False
                #     mario.frame = 0
                #     mario.slowFrame = 0
            # 아래 방향키 떼기
            elif event.key == SDLK_DOWN:
                if mario.status == c_state.S_Down:
                    mario.status = c_state.S_Idle
                    mario.isWalk = False
                    mario.frame = 0
                    mario.slowFrame = 0


# Initialize
#
open_canvas()
# 백그라운드
background = BG()
stat = StatBar()

# 마리오 객체를 생성
mario = Character()

# 지형
tiles = []
def make_tile(xPos, yPos, type):
    newTile = Tile()
    newTile.x, newTile.y = xPos, yPos
    newTile.type = type

    tiles.append(newTile)
for i in range(100):
    make_tile(i*30, 90, "Grass")

for i in range(100):
    make_tile(i*30, 60, "Dirt")

# 박스
boxes = []
def make_box(xPos, yPos, box_type):
    newBox = Box_Question()
    newBox.x, newBox.y = xPos, yPos
    newBox.itemValue = box_type

    boxes.append(newBox)
make_box(200, 200, 2)
make_box(500, 320, 0)
make_box(530, 320, 0)
make_box(600, 320, 0)

# 벽돌
bricks = []
def make_brick(xPos, yPos):
    newBrick = Brick()
    newBrick.x, newBrick.y = xPos, yPos

    bricks.append(newBrick)
for i in range(10):
    make_brick(450+i*30, 200)


# 아이템
fireflower1 = Fireflower() # 꽃

coin1 = Coin() # 코인

# 액션
fire1 = Fire()


#=== Main Loop
#
running = True


while running:

    handle_events() # 키 입력 받아들이는 처리

    mario.update()

    for box in boxes:
        box.update()

    for brick in bricks:
        brick.update()

    fireflower1.update()

    #=== Render
    clear_canvas()
    background.draw()
    stat.draw()

    mario.draw()

    for tile in tiles:
        tile.draw()

    for box in boxes:
        box.draw()

    for brick in bricks:
        brick.draw()

    fireflower1.draw()

    fire1.draw()

    coin1.draw()

    update_canvas()

    delay(0.01)

