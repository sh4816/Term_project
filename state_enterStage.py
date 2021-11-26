import game_framework
from pico2d import *

# 게임 데이터
import game_data as G_data

# 변경되는 맵
import state_map1
import state_map2_1
import state_map2_2
import state_map2_3
import state_map3
import state_mapF_Boss

name = "EnteringState"
image = None
image_numbers = None
loading_time = 0.0

one_number_sizeW, one_number_sizeH = 60, 75


def enter():
    global image, image_numbers
    image = load_image('img_EnterStage.png')
    image_numbers = load_image('numbers_EnterStage.png')


def exit():
    global image
    del(image)


def update():
    global loading_time

    if (loading_time > 1.0):
        loading_time = 0

        # 입장한 스테이지로 이동
        if G_data.gameData.cur_stage == 1:
            game_framework.change_state(state_map1)
        elif G_data.gameData.cur_stage == 2:
            game_framework.change_state(state_map2_1)
        elif G_data.gameData.cur_stage == 3:
            game_framework.change_state(state_map3)
        elif G_data.gameData.cur_stage == 4:
            game_framework.change_state(state_mapF_Boss)
    else:
        loading_time += game_framework.frame_time


def draw():
    global image
    clear_canvas()

    # === 배경 이미지
    image.draw(400, 300)

    # === 현재 스테이지 숫자
    image_numbers.clip_draw(G_data.gameData.cur_stage * one_number_sizeW, 0
                            , one_number_sizeW, one_number_sizeH, 475, 365)
    # === 남은 life 숫자
    # 십의 자리
    if G_data.gameData.life >= 10:
        image_numbers.clip_draw(G_data.gameData.life // 10 * one_number_sizeW, 0
                                , one_number_sizeW, one_number_sizeH, 475, 265)
    # 일의 자리
    if G_data.gameData.life >= 10:
        image_numbers.clip_draw(G_data.gameData.life % 10 * one_number_sizeW, 0
                                , one_number_sizeW, one_number_sizeH, 520, 265)
    else:
        image_numbers.clip_draw(G_data.gameData.life % 10 * one_number_sizeW, 0
                                , one_number_sizeW, one_number_sizeH, 475, 265)

    update_canvas()


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            # 종료
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()


def pause(): pass


def resume(): pass




