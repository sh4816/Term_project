# Player
from pico2d import *
from State import *
import Map_Tile
import Map_Box
import Map_Brick
import Item_Coin
import Item_TransForm

# 캐릭터
class Character:
    def __init__(self):
        # 변신 관련 변수
        self.transform = 1          # 변신 상태 (0: 기본, 1: 슈퍼마리오, 2: 파이어마리오)

        # 기본
        self.image = load_image('Mario.png')
        self.frameX, self.frameY = 0, 0       # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)

        self.x, self.y = 500, 250
        self.frame = 0
        self.slowFrame = 0
        self.status = c_state.S_Idle
        # < Mario Status >
        # 0: Idle(1), 1: Walk(2), 2: Hit(1), 3: Jump(1), 4: Dash(4)
        # 5: Down(1), 6: Slide/GroundPound(1), 7: Stand(1), 8: Kick(4), 9: Climb(2)
        # 10: Action/Attack(standard:X,super:X,fire:2)
        self.isLeft = False         # 왼쪽을 보고 있는지
        self.isOnGround = 0         # 땅 위에 있는지 (0: 땅 위에 없음, 1 이상: 땅 위에 있음)
        self.doubleInput = False

       # 걷기 관련 변수
        self.isWalk = False         # 걷는 중인지
        self.lBlocked = False       # 막혀 있는지
        self.rBlocked = False

        # 점프 관련 변수
        self.jumpHeight = 15
        self.isUnderBlock = 0       # 상단이 블록으로 막혀있는지 (0: 막혀있지 않음, 1 이상: 막혀있음)
        self.jump_collipseYPos = 0
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

        # 액션/공격 관련 변수
        self.act = False            # 액션 중인지
        self.act_Delay = 0          # 액션 후딜레이

    def update(self):
        # Out of Window 체크
        if self.y < 0:
            # Life 업데이트 후 Life감소 추가 예정.
            self.x, self.y = 400, 300
            print('사망')

        # 변신 아이템 충돌체크
        for t_item in Item_TransForm.t_items:
            if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                             t_item.frameX, t_item.frameY, t_item.x, t_item.y, True):
                if self.transform < t_item.itemValue:       # 변신 아이템보다 현재 상태가 하위 상태일때
                    self.transform = t_item.itemValue
                    self.status = c_state.S_Transform
                    self.slowFrame = 0
                    self.frame = 0

                # 점수추가 (추가예정)
                print('Score up')
                Item_TransForm.t_items.remove(t_item)  # 객체 삭제

        # 이미지 체크
        if self.transform == 0:
            if self.isLeft:
                self.image = load_image('MarioL.png')  # 왼쪽을 보고 있는 리소스
            else:
                self.image = load_image('Mario.png')   # 오른쪽을 보고 있는 리소스
            self.frameX, self.frameY = 30, 40          # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        elif self.transform == 1:
            if self.isLeft:
                self.image = load_image('MarioL_super.png')  # 왼쪽을 보고 있는 리소스
            else:
                self.image = load_image('Mario_super.png')   # 오른쪽을 보고 있는 리소스
            self.frameX, self.frameY = 40, 60                # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        elif self.transform == 2:
            if self.isLeft:
                self.image = load_image('MarioL_fire.png')   # 왼쪽을 보고 있는 리소스
            else:
                self.image = load_image('Mario_fire.png')    # 오른쪽을 보고 있는 리소스
            self.frameX, self.frameY = 40, 60                # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)


        # 상태 체크
        #=== Idle
        if self.status == c_state.S_Idle:
            # 1. 충돌하면 1을 더한다.
            for tile in Map_Tile.tiles:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 tile.frameX, tile.frameY, tile.x, tile.y, True):
                    self.isOnGround += 1
            for box in Map_Box.boxes:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 box.frameX, box.frameY, box.x, box.y, True):
                    self.isOnGround += 1
            for brick in Map_Brick.bricks:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 brick.frameX, brick.frameY, brick.x, brick.y, True):
                    self.isOnGround += 1
            # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
            if self.isOnGround == 0:
                self.status = c_state.S_Jump
                self.frame = 0

                self.isLeap = False
                self.isFall = True
            else:
                self.isOnGround = 0
        #=== Walk
        elif self.status == c_state.S_Walk:
            # 이동
            if self.isWalk:
                self.slowFrame += 1
                self.frame = (self.slowFrame // 3) % 2
                if self.isLeft:
                    self.x -= 5
                else:
                    self.x += 5


            # 1. 충돌하면 1을 더한다.
            for tile in Map_Tile.tiles:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 tile.frameX, tile.frameY, tile.x, tile.y, True):
                    self.isOnGround += 1
            for box in Map_Box.boxes:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 box.frameX, box.frameY, box.x, box.y, True):
                    self.isOnGround += 1
            for brick in Map_Brick.bricks:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 brick.frameX, brick.frameY, brick.x, brick.y, True):
                    self.isOnGround += 1
            # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
            if self.isOnGround == 0:
                self.status = c_state.S_Jump
                self.frame = 0

                self.isLeap = False
                self.isFall = True
                self.move_in_air = True
            else:
                self.isOnGround = 0

        #=== Hit
        elif self.status == c_state.S_Hit:
            pass#미구현
        #=== Jump
        elif self.status == c_state.S_Jump:
            # 공중에서 좌우로 움직이는 거
            if self.move_in_air:
                # 충돌체크 ( 이동 예정인 좌표와 오브젝트, 현재 좌표X )
                # 1. 충돌하면 1을 더한다.
                for tile in Map_Tile.tiles:
                    if collipseCheck(self.frameX, self.frameY, self.x, self.y + self.jumpHeight,
                                     tile.frameX, tile.frameY, tile.x, tile.y, False):
                        if self.y - self.frameY / 2 < tile.y + tile.frameY / 2:
                            if self.x + self.frameX/2 >= tile.x - tile.frameX/2:
                                self.rBlocked = True
                            elif self.x - self.frameX/2 <= tile.x + tile.frameX/2:
                                self.lBlocked = True
                        # else:
                        #     self.isBlocked = False

                for box in Map_Box.boxes:
                    if collipseCheck(self.frameX, self.frameY, self.x, self.y + self.jumpHeight,
                                       box.frameX, box.frameY, box.x, box.y, False):
                        if self.y - self.frameY/2 < box.y + box.frameY/2:
                            if self.x + self.frameX / 2 >= box.x - box.frameX / 2:
                                self.rBlocked = True
                            elif self.x - self.frameX / 2 <= box.x + box.frameX / 2:
                                self.lBlocked = True

                for brick in Map_Brick.bricks:
                    if collipseCheck(self.frameX, self.frameY, self.x, self.y + self.jumpHeight,
                                     brick.frameX, brick.frameY, brick.x, brick.y, False):
                        if self.y - self.frameY / 2 < brick.y + brick.frameY / 2:
                            if self.x + self.frameX / 2 >= brick.x - brick.frameX / 2:
                                self.rBlocked = True
                            elif self.x - self.frameX / 2 <= brick.x + brick.frameX / 2:
                                self.lBlocked = True

                # 2. 하나라도 충돌했다면 isUnderBlock는 0이 아니게 된다는 점 이용
                # 충돌한게 없을 때만 이동 가능
                if self.isLeft:
                    if not self.lBlocked:
                        if self.dashJump:
                            self.x -= 8
                        else:
                            self.x -= 5
                else:
                    if not self.rBlocked:
                        if self.dashJump:
                            self.x += 8
                        else:
                            self.x += 5

                self.lBlocked = self.rBlocked = False

            if self.isLeap:
                # 충돌체크 ( 이동 예정인 좌표와 오브젝트, 현재 좌표X )
                # 1. 충돌하면 1을 더한다.
                for tile in Map_Tile.tiles:
                    if collipseCheck(self.frameX, self.frameY, self.x, self.y + self.jumpHeight,
                                     tile.frameX, tile.frameY, tile.x, tile.y, False):
                        if tile.x - tile.frameX/2 <= self.x <= tile.x + tile.frameX/2:
                            if self.y <= tile.y - tile.frameX/2:
                                self.isUnderBlock += 1
                                self.jump_collipseYPos = tile.y - tile.frameY/2 - self.frameY/2
                for box in Map_Box.boxes:
                    if collipseCheck(self.frameX, self.frameY, self.x, self.y + self.jumpHeight,
                                       box.frameX, box.frameY, box.x, box.y, False):
                        if box.x - box.frameX/2 <= self.x <= box.x + box.frameX/2:
                            if self.y <= box.y - box.frameX/2:
                                self.isUnderBlock += 1
                                self.jump_collipseYPos = box.y - box.frameY/2 - self.frameY/2

                            if not box.isUsed:
                                if box.itemValue == 0:
                                    Item_Coin.make_coins(box.x, box.y + box.frameY/2 + 20, True)
                                elif box.itemValue == 1 or box.itemValue == 2:
                                    Item_TransForm.make_titem(box.x, box.y + box.frameY / 2 + 10, box.itemValue)


                                box.isUsed = True
                for brick in Map_Brick.bricks:
                    if collipseCheck(self.frameX, self.frameY, self.x, self.y + self.jumpHeight,
                                     brick.frameX, brick.frameY, brick.x, brick.y, False):
                        if brick.x - brick.frameX/2 <= self.x <= brick.x + brick.frameX/2:
                            if self.y <= brick.y - brick.frameX/2:
                                self.isUnderBlock += 1
                                self.jump_collipseYPos = brick.y - brick.frameY/2 - self.frameY/2
                                # 충돌한 벽돌은 삭제됨
                                Map_Brick.bricks.remove(brick)
                # 2. 하나라도 충돌했다면 isUnderBlock는 0이 아니게 된다는 점 이용
                if not self.isUnderBlock == 0:
                    self.y = self.jump_collipseYPos - 1
                    self.jumpHeight = 0
                    self.isUnderBlock = 0

                # 최대 높이에 도달했거나, 상단이 물체로 가로막힌 경우 낙하를 시작한다.
                if self.jumpHeight <= 0:
                    self.isLeap = False
                    self.isFall = True
                    self.jumpHeight = 0
                else:
                    self.y += self.jumpHeight
                    self.jumpHeight -= 1

            elif self.isFall:
                self.y -= self.jumpHeight
                self.jumpHeight += 1

                # 충돌체크
                # 1. 충돌하면 1을 더한다.
                for tile in Map_Tile.tiles:
                    if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                     tile.frameX, tile.frameY, tile.x, tile.y, True):
                        self.isOnGround += 1
                        self.gp_EndHeight = tile.y + tile.frameY/2 + self.frameY/2
                for box in Map_Box.boxes:
                    if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                       box.frameX, box.frameY, box.x, box.y, True):
                        self.isOnGround += 1
                        self.gp_EndHeight = box.y + box.frameY/2 + self.frameY/2
                for brick in Map_Brick.bricks:
                    if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                     brick.frameX, brick.frameY, brick.x, brick.y, True):
                        self.isOnGround += 1
                        self.gp_EndHeight = brick.y + brick.frameY/2 + self.frameY/2
                # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
                if self.isOnGround == 0:
                    self.isOnGround = 0
                else:
                    self.isFall = False
                    self.dashJump = False
                    if self.move_in_air:
                        if self.dashJump:
                            self.status = c_state.S_Dash
                            self.dash = True
                            self.dashJump = False
                        else:
                            self.status = c_state.S_Walk
                        self.isWalk = True
                        self.move_in_air = False
                        self.frame = 0
                    else:
                        self.status = c_state.S_Idle
                        self.isWalk = False
                        self.move_in_air = False
                        self.frame = 0

                    self.jumpHeight = 15
                    self.isOnGround = 0

                    self.y = self.gp_EndHeight - 5
        #=== Dash
        elif self.status == c_state.S_Dash:
            # 이동
            self.frame = (self.frame + 1) % 4
            if self.isLeft:
                self.x -= 10
            else:
                self.x += 10


            # 1. 충돌하면 1을 더한다.
            for tile in Map_Tile.tiles:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 tile.frameX, tile.frameY, tile.x, tile.y, True):
                    self.isOnGround += 1
            for box in Map_Box.boxes:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 box.frameX, box.frameY, box.x, box.y, True):
                    self.isOnGround += 1
            for brick in Map_Brick.bricks:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 brick.frameX, brick.frameY, brick.x, brick.y, True):
                    self.isOnGround += 1
            # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
            if self.isOnGround == 0:
                self.status = c_state.S_Jump
                self.frame = 0

                self.isLeap = False
                self.isFall = True
                self.move_in_air = True
            else:
                self.isOnGround = 0
        #=== Down
        elif self.status == c_state.S_Down:
            pass
        #=== GroundPound
        elif self.status == c_state.S_GP:
            self.gp_accel += 0.98 * 3

            # 충돌체크
            # 1. 충돌하면 1을 더한다.
            for tile in Map_Tile.tiles:
               if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                tile.frameX, tile.frameY, tile.x, tile.y, True):
                    self.isOnGround += 1
                    self.gp_EndHeight = tile.y + tile.frameY/2 + self.frameY/2
                    if self.gp:
                        self.gp_delay = 4  # 그라운드파운드 후딜레이
                        self.gp = False
            for box in Map_Box.boxes:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                   box.frameX, box.frameY, box.x, box.y, True):
                    self.isOnGround += 1
                    self.gp_EndHeight = box.y + box.frameY/2 + self.frameY/2
                    if self.gp:
                        self.gp_delay = 4  # 그라운드파운드 후딜레이
                        self.gp = False

                    if not box.isUsed:
                        if box.itemValue == 0:
                            Item_Coin.make_coins(box.x, box.y + box.frameY / 2 + 20, True)
                        elif box.itemValue == 1 or box.itemValue == 2:
                            Item_TransForm.make_titem(box.x, box.y + box.frameY / 2 + 10, box.itemValue - 1)


                        box.isUsed = True
            for brick in Map_Brick.bricks:
                if collipseCheck(self.frameX, self.frameY, self.x, self.y,
                                 brick.frameX, brick.frameY, brick.x, brick.y, True):
                    self.gp_accel /= 2
                    # 충돌한 벽돌은 삭제됨
                    Map_Brick.bricks.remove(brick)

            # 2. 하나라도 충돌했다면 isOnGround는 0이 아니게 된다는 점 이용
            if self.isOnGround == 0:
                self.y -= self.gp_accel
            else:
                self.y = self.gp_EndHeight
                # 착지 후 딜레이 계산
                self.gp_delay -= 1
                if self.gp_delay == 0:
                    self.status = c_state.S_Idle
                    self.frame = 0

                    self.isLeap = False
                    self.isFall = False
                    gp_Collipse = True
                    gp_gapHeight = 0
                    self.gp_accel = 0
                    self.jumpHeight = 15
                    self.gp_delay = 3
        #=== Action/Attack
        elif self.status == c_state.S_Action:
            self.act_Delay -= 1
            self.slowFrame += 1
            self.frame = (self.slowFrame // 2) % 2

            fire1.isRendered = True
            fire1.x, fire1.y = self.x, self.y
            if self.isLeft: fire1.dir = 0
            else:           fire1.dir = 1

            if self.act_Delay == 0:
                #test
                self.status = c_state.S_Idle
                self.frame = 0

                self.slowFrame = 0
                self.act = False
        #=== TransForm
        elif self.status == c_state.S_Transform:
            self.slowFrame += 1
            self.frame = (self.slowFrame // 2) % 5

            if self.slowFrame > 10:
                if self.isWalk:
                    self.status = c_state.S_Walk
                    self.isWalk = True
                    self.dash = self.dashJump = self.isLeap \
                        = self.isFall = self.move_in_air = self.gp = False
                else:
                    self.status = c_state.S_Idle
                    self.isWalk = self.dash = self.dashJump = self.isLeap\
                        = self.isFall = self.move_in_air = self.gp = False

    def draw(self):
        if self.transform == 0:
            self.image.clip_draw(self.frame * self.frameX, (10 - (self.status.value - 1)) * self.frameY
                                 , self.frameX, self.frameY, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * self.frameX, (11 - (self.status.value - 1)) * self.frameY
                                 , self.frameX, self.frameY, self.x, self.y)



def collipseCheck(obj1_w, obj1_h, obj1_cx, obj1_cy, obj2_w, obj2_h, obj2_cx, obj2_cy, isPlayer):
    # 두 사각형의 상하좌우 변
    r1_L, r1_R = obj1_cx - obj1_w/2, obj1_cx + obj1_w/2
    r1_T, r1_B = obj1_cy + obj1_h/2, obj1_cy - obj1_h/2
    r2_L, r2_R = obj2_cx - obj2_w/2, obj2_cx + obj2_w/2
    r2_T, r2_B = obj2_cy + obj2_h/2, obj2_cy - obj2_h/2

    if isPlayer:    # Player의 리소스 파일 크기때문에 플레이어 발 아래에 발판이 없는 것 처럼 보이지만, 충돌처리가 되는 경우 방지.
        r1_L += 13
        r1_R -= 13

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