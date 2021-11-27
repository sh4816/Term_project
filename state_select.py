import game_framework
from pico2d import *
import enum

# Game Data
import game_data

# Map
import state_enterStage

name = "TitleState"
image = None
image_mario = None
image_lock = None

# 변신 상태
class P_Transform(enum.IntEnum):
    T_Basic = 0
    T_Super = enum.auto()
    T_Fire = enum.auto()

def enter():
    global image, image_mario, image_lock
    image = load_image('select.png')

    if game_data.gameData.transform == P_Transform.T_Basic:
        image_mario = load_image('Mario.png')
    elif game_data.gameData.transform == P_Transform.T_Super:
        image_mario = load_image('Mario_super.png')
    elif game_data.gameData.transform == P_Transform.T_Fire:
        image_mario = load_image('Mario_fire.png')

    image_lock = load_image('lock.png')


def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            # 종료
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            # 입장
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                if game_data.gameData.cur_stage <= game_data.gameData.unlocked_stage:   # 잠겨있지 않은 맵에만
                    game_framework.change_state(state_enterStage)
                else:
                    print('잠겨있는 맵')
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                if game_data.gameData.cur_stage > 1:
                    game_data.gameData.cur_stage -= 1
                else:
                    print('처음 스테이지')
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                if game_data.gameData.cur_stage < 4:
                    game_data.gameData.cur_stage += 1
                else:
                    print('마지막 스테이지')

            # 아래 3개는 치트키임
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
                print('치트키 - 해금 1')
                game_data.gameData.unlocked_stage = 1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
                print('치트키 - 해금 2')
                game_data.gameData.unlocked_stage = 2
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
                print('치트키 - 해금 3')
                game_data.gameData.unlocked_stage = 3
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_4):
                print('치트키 - 해금 F')
                game_data.gameData.unlocked_stage = 4


def draw():
    clear_canvas()
    image.draw(400, 300)

    for i in range(4 - game_data.gameData.unlocked_stage, 0, -1):
        image_lock.draw(200 + 150 * (4 - i) + 25, 300 - 20)
    # if game_data.gameData.unlocked_stage == 1:
    #     image_lock.draw(480, 200)
    #     image_lock.draw(630, 200)
    # elif game_data.gameData.unlocked_stage == 2:
    #     image_lock.draw(630, 200)

    drawX = 200 + 150 * (game_data.gameData.cur_stage - 1)
    if game_data.gameData.transform == int(P_Transform.T_Basic):
        image_mario.clip_draw(0, 270, 30, 30, drawX + 25, 300 - 20)
    else:
        image_mario.clip_draw(0, 540, 30, 60, drawX + 25, 300 - 20)

    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass






