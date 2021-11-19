from pico2d import *

show_bb = False

class Castle:
    image = None

    def __init__(self):  # 생성자
        self.frameX, self.frameY = 210, 180
        self.x, self.y = 0, 0
        self.scrollX = 0

        self.door_frameX, self.door_frameY = 30, 60

        self.image = load_image('castle.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.scrollX, self.y)

        # bounding box
        global show_bb
        if show_bb:
            # 성
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)
            # # 문
            # draw_rectangle(self.x - self.door_frameX / 2 - self.scrollX, self.y - self.door_frameY/4
            #                , self.x + self.door_frameX / 2 - self.scrollX, self.y - self.door_frameY)

class Door:
    image = None
    # Door는 castle에 있는 문으로 단지 문의 위치값을 사용하는 계산을 하기위해 만들어진 클래스로 이미지를 따로 그려줄 필요가 없다.

    def __init__(self):
        self.frameX, self.frameY = 30, 60
        self.x, self.y = 0, 0
        self.scrollX = 0

    def update(self):
        pass

    def draw(self):
        # 바운딩박스만 그려준다.
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y - self.frameY / 4
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY)



# 객체 생성 함수
doors = []
castles = []
def makeDoor(xPos, yPos):
    newDoor = Door()
    newDoor.x, newDoor.y = xPos, yPos
    doors.append(newDoor)


def makeCastle(xPos, yPos):
    newCastle = Castle()
    newCastle.x, newCastle.y = xPos, yPos
    castles.append(newCastle)
    makeDoor(newCastle.x, newCastle.y)  # 문 생성


def removeAll():
    print('성&문 전체 삭제')
    for obj in castles:
        castles.remove(obj)
    for obj in doors:
        doors.remove(obj)