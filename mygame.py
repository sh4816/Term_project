import game_framework
import pico2d

import main_state
import state_intro
import state_map1

pico2d.open_canvas(800, 600)
# game_framework.run(state_map1)
game_framework.run(state_intro)
pico2d.close_canvas()