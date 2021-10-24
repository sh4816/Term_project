from pico2d import *

#BackGround
class BG:
    def __init__(self): # 생성자
        self.image = load_image('Background_1.png')
        self.value = ""

    def draw(self):
        if self.value == "Map1":
            self.image = load_image('Background_1.png')

        self.image.draw(400, 300)


bg = BG
def make_bg(val):
    bg.value = val