from pico2d import *

show_bb = None

# 트리거
class Trigger:
    def __init__(self):  # 생성자
        self.frameX, self.frameY = 30, 30  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)
        self.x, self.y = 0, 0
        self.scrollX = 0
        self.type = None
        # map : 맵 이동 관련
        # 1. map_select: 선택 화면으로 이동하는 이벤트 발생 트리거
        # 2. map_map1: 맵1로 이동하는 이벤트 발생 트리거
        #

        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        # bounding box
        global show_bb
        if show_bb:
            draw_rectangle(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2
                           , self.x + self.frameX / 2 - self.scrollX, self.y - self.frameY / 2)
            self.font.draw(self.x - self.frameX / 2 - self.scrollX, self.y + self.frameY / 2 + 10, 'Trigger', (0, 0, 255))


triggers = []
# 트리거 추가
def makeTrigger(xPos, yPos, trigger_type):
    newTrigger = Trigger()
    newTrigger.x, newTrigger.y = xPos, yPos
    newTrigger.type = trigger_type

    triggers.append(newTrigger)
    print('Trigger 생성 - Pos: ' + str((newTrigger.x, newTrigger.y)) + ', type: ' + str(newTrigger.type))

# 트리거 삭제
def remove_a_trigger(target):
    triggers.remove(target)

def remove_all_triggers():
    for target in triggers:
        triggers.remove(target)

