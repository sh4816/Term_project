from pico2d import *

#BackGround
class BG:
    image = None

    def __init__(self): # 생성자
        self.image = load_image('BG.png')
        self.x = 0
        self.scrollX = 0
        self.overX = 0      # 이미지를 가져오는 범위가 기존 이미지를 얼마만큼 벗어나는지
        self.value = ""

        self.image = load_image('BG.png')
        self.image1 = load_image('BG1.png')
        self.image2 = load_image('BG2.png')
        self.image3 = load_image('BG3.png')
        self.imageB1 = load_image('BGB1.png')
        self.imageF = load_image('BGFinal.png')

    def update(self):
        pass

    def draw(self):
        if self.value == "map1":
            self.image = self.image1
        elif self.value == "map2_1":
            self.image = self.image2
        elif self.value == "map2_2":
            self.image = self.imageB1
        elif self.value == "map2_3":
            self.image = self.image3
        elif self.value == "map3":
            self.image = self.imageF

        # 작동 방식: 800x600 크기의 중심을 왼쪽으로 이동시키면서 화면 왼쪽 바깥으로 잘려나간 부분을 화면 오른쪽에서 다시 그려준다.
        # clib_draw: 렌더링 시작위치(x,y), 이미지에서 가져올 범위(w,h), 피봇(cx,cy), 렌더링 사이즈(w,h) 인거같기도...?
        # 그림 1: 윈도우를 벗어나지 않은 부분
        self.image.clip_draw(0, 0, 800, 600, 400 - int(self.scrollX) % 800, 300)
        # 그림 2: 윈도우의 왼쪽으로 벗어난 부분
        self.image.clip_draw(0, 0, int(self.scrollX) % 800, 600, 800 - int(self.scrollX) % 800 / 2, 300)
