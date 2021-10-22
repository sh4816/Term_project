from enum import *

class C_state(Enum):
    S_Idle = auto()
    S_Walk = auto()
    S_Hit = auto()
    S_Jump = auto()
    S_Dash = auto()
    S_Down = auto()
    S_GP = auto()
    S_Stand = auto()
    S_Kick = auto()
    S_Climb = auto()
    S_Action = auto()

c_state = C_state