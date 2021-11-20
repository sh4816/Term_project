import game_framework
import pico2d

import state_intro
import state_map2_1

pico2d.open_canvas(800, 600)
#game_framework.run(state_map2_1)    # test때 바로 이동할 맵 정상 작동을 할때에 해당 줄을 주석처리하고 아래 줄을 실행
game_framework.run(state_intro)
pico2d.close_canvas()