import game_framework
import pico2d

import main_state
import state_map1

pico2d.open_canvas(800, 600)
game_framework.run(state_map1)
pico2d.close_canvas()