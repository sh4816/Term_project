from pico2d import *
import enum

# 디버그, 상태가 변할 때마다 변경내용을 저장해준다.
histroy = []

# Event 종류
LEFT_DOWN, LEFT_UP, RIGHT_DOWN, RIGHT_UP,\
    Z_DOWN, Z_UP, X_DOWN, X_UP, C_DOWN, C_UP,\
    DEBUG_KEY = range(11)

event_name = ['LEFT_DOWN', 'LEFT_UP', 'RIGHT_DOWN', 'RIGHT_UP',\
    'Z_DOWN', 'Z_UP', 'X_DOWN', 'X_UP', 'C_DOWN', 'C_UP',\
    'DEBUG_KEY']

key_event_table = {
    (SDL_KEYDOWN,SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,

    (SDL_KEYDOWN, SDLK_z): Z_DOWN,
    (SDL_KEYUP, SDLK_z): Z_UP,
    (SDL_KEYDOWN, SDLK_x): X_DOWN,
    (SDL_KEYUP, SDLK_x): X_UP,
    (SDL_KEYDOWN, SDLK_c): C_DOWN,
    (SDL_KEYUP, SDLK_c): C_UP,

    (SDL_KEYDOWN, SDLK_v): DEBUG_KEY
}


# 변신 상태 enum
class Transform_State(enum.IntEnum):
    StandardM = enum.auto()
    SuperM = enum.auto()
    FireM = enum.auto()


# Player의 상태(States) 클래스

class S_Idle:
    def enter(player, event):
        # 이미지 설정
        if player.image == None:        # 변신상태가 바뀌면 image가 None으로 바뀌게되고 이때에만 이미지를 로딩한다.
            if player.dir == 1:
                if player.transform == Transform_State.StandardM:
                    player.image = load_image('Mario.png')
                elif player.transform == Transform_State.SuperM:
                    player.image = load_image('Mario_super.png')
                elif player.transform == Transform_State.FireM:
                    player.image = load_image('Mario_fire.png')
            else:
                if player.transform == Transform_State.StandardM:
                    player.image = load_image('MarioL.png')
                elif player.transform == Transform_State.SuperM:
                    player.image = load_image('MarioL_super.png')
                elif player.transform == Transform_State.FireM:
                    player.image = load_image('MarioL_fire.png')

        # 방향 설정
        if event == LEFT_DOWN:
            player.velocity -= 1
        elif event == LEFT_UP:
            player.velocity += 1
        elif event == RIGHT_DOWN:
            player.velocity += 1
        elif event == RIGHT_UP:
            player.velocity -= 1

        player.frameY = 0
        #player.timer = 1000 #이거 나중에 한동안 키입력이 없을때 하늘쳐다보는 애니메이션 출력할때 쓸 예정!


    def exit(player, event):
        pass


    def do(player):
        pass
        # player.timer -= 1
        # if player.timer == 0:
        #     player.add_event(여기에 event이름 넣으면됨!)


    def draw(player):
        player.image.clip_draw(player.frameX * player.frameW, 0, player.frameW, player.frameY, player.x, player.y)



class S_Walk:

    def enter(player, event):
        if event == LEFT_DOWN:
            player.velocity -= 1
        elif event == LEFT_UP:
            player.velocity += 1
        elif event == RIGHT_DOWN:
            player.velocity += 1
        elif event == RIGHT_UP:
            player.velocity -= 1

        player.dir = player.velocity

    def exit(player, event):
        pass

    def do(player):
        player.frame = (player.frame + 1) % 2
        # player.timer -= 1
        player.x += player.velocity
        player.x = clamp(25, player.x, 1600 - 25)
        
    def draw(player):
        if player.velocity == 1:
            player.image.clip_draw(player.frame * )


# Player 클래스
class Player:

    def __init__(self):
        self.x, self.y = 100, 100
        self.image = load_image('Mario.png')
        self.dir = 1
        self.velocity = 0
        self.transform = 0  # 마리오, 슈퍼마리오, 파이어마리오
        self.frameX, frameY = 0, 0
        self.frameW, frameH = 0, 0  # 한 프레임 크기 (캐릭터 리소스 수정 시 여기 부분 수정하면됨!)

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                # 일단 아래 문장을 실행해보기..
                history.append( (self.cur_state.__name__, event_name[event]) )
                self.cur_state = next_state_table[self.cur_state][event]
            except:
                # 만약 문제가 발생하면, 아래를 실행.
                # 어떤 정보가 필요?: 현재 상태 정보, 어떤 이벤트였는지
                print('State: ' + self.cur_state.__name__ + ' Event: ' + event_name[event])
                exit(-1) # 강제 종료

            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if DEBUG_KEY == key_event:
                print(history[-10:])
            else:
                self.add_event(key_event)
