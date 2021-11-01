from pico2d import *
from State import *
import Player
import ScrollManager as scrollMgr
import MapEditor
import Map_Background
import Map_Tile
import Map_Box
import Map_Brick
import Map_Pipe
import Item_Coin
import Item_TransForm


open_canvas()
bg = Map_Background.BG()
bg.value = "map1"

#=== Initialize

# 마리오 객체를 생성
mario = Player.Character()

# 맵 불러오기
MapEditor.editMap("map1")

#=== Handle Events
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
                print('ScrollX: ' + str(mario.scrollX))
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


#=== Main Loop
running = True

while running:
    # 키 입력 받아들이는 처리
    handle_events()


    #=== Update
    mario.scrollX = scrollMgr.getScrollX("Map1", mario)
    mario.update()

    bg.scrollX = scrollMgr.getScrollX("Map1", mario)#

    for tile in Map_Tile.tiles:
        tile.scrollX = scrollMgr.getScrollX("Map1", mario)

    for box in Map_Box.boxes:
        box.update()
        box.scrollX = scrollMgr.getScrollX("Map1", mario)

    for brick in Map_Brick.bricks:
        brick.update()
        brick.scrollX = scrollMgr.getScrollX("Map1", mario)

    for pipe in Map_Pipe.pipes:
        pipe.update()
        pipe.scrollX = scrollMgr.getScrollX("Map1", mario)

    for coin in Item_Coin.coins:
        coin.scrollX = scrollMgr.getScrollX("Map1", mario)

    for t_item in Item_TransForm.t_items:
        t_item.update()
        t_item.scrollX = scrollMgr.getScrollX("Map1", mario)


    #=== Render
    clear_canvas()

    bg.draw()

    mario.draw()

    for tile in Map_Tile.tiles:
        tile.draw()

    for box in Map_Box.boxes:
        box.draw()

    for brick in Map_Brick.bricks:
        brick.draw()

    for pipe in Map_Pipe.pipes:
        pipe.draw()

    for coin in Item_Coin.coins:
        coin.draw()

    for t_item in Item_TransForm.t_items:
        t_item.draw()


    update_canvas()
    # delay(0.001)