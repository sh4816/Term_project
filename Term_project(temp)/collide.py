import enum

# 충돌체크 함수
def collideCheck(player, obj):
    # 충돌Rect
    p_left, p_right = player.x - player.frameX/2, player.x + player.frameX/2
    p_top, p_bottom = player.y + player.frameY, player.y - player.frameY/2

    o_left, o_right = obj.x - obj.frameX / 2, obj.x + obj.frameX / 2
    o_top, o_bottom = obj.y + obj.frameY / 2, obj.y - obj.frameY / 2

    # player 윗변 충돌 검사
    if o_bottom <= p_top <= o_top:        # player충돌rect 윗변이 obj 안에 있을 때
        if o_left <= p_left <= o_right:   # player충돌rect 왼쪽이 obj 안에 있음
            return "top"
        if o_left <= p_right <= o_right:  # player충돌rect 오른쪽이 obj 안에 있음
            return "top"
        if o_left >= p_left and o_right <= p_right:   # player충돌rect 가 obj의 너비를 포함하는 경우
            return "top"

    # player 아랫변 충돌 검사
    if o_bottom <= p_bottom <= o_top:     # player충돌rect 아랫변이 obj 안에 있을 때
        if o_left <= p_left <= o_right:   # player충돌rect 왼쪽이 obj 안에 있음
            return "bottom"
        if o_left <= p_right <= o_right:  # player충돌rect 오른쪽이 obj 안에 있음
            return "bottom"
        if o_left >= p_left and o_right <= p_right:   # player충돌rect 가 obj의 너비를 포함하는 경우
            return "bottom"

    # player 왼쪽 충돌 검사
    if o_left <= p_left <= o_right:       # player충돌rect 왼쪽이 obj 안에 있을 때
        if o_bottom <= p_top <= o_top:    # player충돌rect 윗변이 obj 안에 있음
            return "left"
        if o_bottom <= p_bottom <= o_top: # player충돌rect 아랫변이 obj 안에 있음
            return "left"

    # player 왼쪽 충돌 검사
    if o_left <= p_right <= o_right:       # player충돌rect 오른쪽이 obj 안에 있을 때
        if o_bottom <= p_top <= o_top:    # player충돌rect 윗변이 obj 안에 있음
            return "right"
        if o_bottom <= p_bottom <= o_top: # player충돌rect 아랫변이 obj 안에 있음
            return "right"

    return None

def collipseCheck(obj1_w, obj1_h, obj1_cx, obj1_cy, obj2_w, obj2_h, obj2_cx, obj2_cy, isPlayer):
    # 두 사각형의 상하좌우 변
    r1_L, r1_R = obj1_cx - obj1_w/2, obj1_cx + obj1_w/2
    r1_T, r1_B = obj1_cy + obj1_h/2, obj1_cy - obj1_h/2
    r2_L, r2_R = obj2_cx - obj2_w/2, obj2_cx + obj2_w/2
    r2_T, r2_B = obj2_cy + obj2_h/2, obj2_cy - obj2_h/2


    if isPlayer:    # Player의 리소스 파일 크기때문에 플레이어 발 아래에 발판이 없는 것 처럼 보이지만, 충돌처리가 되는 경우 방지.
        r1_L += 13
        r1_R -= 13

    if r1_R > r2_L:                                     # r1의 오른쪽 변이 r2의 왼쪽 변보다 오른쪽에 있을 때
        if not r1_L > r2_R:                             # 단, r1의 왼쪽 변이 r2 보다 오른쪽에 있으면 안된다.
            if r1_B > r2_B and r1_B < r2_T:             # r1의 아랫변이 r2 안에 있는 경우
                return True
            elif r1_T > r2_B and r1_T < r2_T:           # r1의 윗변이 r2 안에 있는 경우
                return True
            elif r1_L > r2_L and r1_L < r2_R:           # r1의 왼쪽 변이 r2 안에 있는 경우
                if not (r1_B > r2_T or r1_T < r2_B):   # 단, r1의 아랫변이 r2 위에 있거나, r1의 윗변이 r2 아래에 있으면 안된다.
                    return True
            elif r1_T > r2_B and r1_B < r2_T:           # r1의 윗변은 r2의 아랫변보다 위에, r1의 아랫변은 r2의 윗변보다 아래에 있는 경우
                if not (r1_L > r2_R or r1_R < r2_L):   # 단, r1의 왼쪽 변이 r2 오른쪽에 있거나, r1의 오른 변이 r2 왼쪽에 있으면 안된다.
                    return True

    if r1_L <= r2_R:                                    # r1의 왼쪽 변이 r2의 오른쪽 변보다 왼쪽에 있을 때
        if not r1_R < r2_L:                             # 단, r1의 오른쪽 변이 r2 보다 왼쪽에 있으면 안된다.
            if r1_B > r2_B and r1_B < r2_T:             # r1의 아랫변이 r2 안에 있는 경우
                return True
            elif r1_T > r2_B and r1_T < r2_T:           # r1의 윗변이 r2 안에 있는 경우
                return True
            elif r1_R > r2_L and r1_R < r2_R:           # r1의 오른쪽 변이 r2 안에 있는 경우
                if not (r1_B > r2_T or r1_T < r2_B):  # 단, r1의 아랫변이 r2 위에 있거나, r1의 윗변이 r2 아래에 있으면 안된다.
                    return True
            elif r1_T > r2_B and r1_B < r2_T:           # r1의 윗변은 r2의 아랫변보다 위에, r1의 아랫변은 r2의 윗변보다 아래에 있는 경우
                if not (r1_L > r2_R or r1_R < r2_L):  # 단, r1의 왼쪽 변이 r2 오른쪽에 있거나, r1의 오른 변이 r2 왼쪽에 있으면 안된다.
                    return True

    if (r1_L > r2_L and r1_L < r2_R) and (r1_R > r2_L and r1_R < r2_R): # r1의 왼쪽, 오른쪽 변 모두 r2 안에 있는 경우
        if not (r1_B > r2_T or r1_T < r2_B):  # 단, r1의 아랫변이 r2 위에 있거나, r1의 윗변이 r2 아래에 있으면 안된다.
            return True

    if (r1_T > r2_B and r1_T < r2_T) and (r1_B > r2_B and r1_B < r2_T): # r1의 윗변, 아랫변 모두 r2 안에 있는 경우
        if not (r1_L > r2_R or r1_R < r2_L):  # 단, r1의 왼쪽 변이 r2 오른쪽에 있거나, r1의 오른 변이 r2 왼쪽에 있으면 안된다.
            return True

    return False    # 위의 모든 경우에 해당하지 않는 경우 False 반환
