from pico2d import *

#BackGround
class BG:
    def __init__(self): # 생성자
        self.image = load_image('BG.png')
        self.value = ""

    def draw(self):
        if self.value == "Map1":
            self.image = load_image('BG.png')

        self.image.draw(400, 300)

