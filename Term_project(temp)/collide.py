import enum

# 충돌체크 함수
def collideCheck(player, obj):
    # 충돌Rect
    p_left, p_right = player.x - player.frameX/2, player.x + player.frameX/2
    p_top, p_bottom = player.y + player.frameY, player.y - player.frameY/2

    o_left, o_right = obj.x - obj.frameX / 2, obj.x + obj.frameX / 2
    o_top, o_bottom = obj.y + obj.frameY / 2, obj.y - obj.frameY / 2

    # 절대로 충돌할 일이 없다면 그냥 함수를 빠져나온다.
    if p_bottom > o_top or p_top < o_bottom or p_right < o_left or p_left > o_right:
        return

    # player 윗변 충돌 검사
    if o_bottom <= p_top <= o_top:                    # player충돌rect 윗변이 obj 안에 있을 때
        if o_left <= p_left <= o_right:               # player충돌rect 왼쪽이 obj 안에 있음
            return "top"
        if o_left <= p_right <= o_right:              # player충돌rect 오른쪽이 obj 안에 있음
            return "top"
        if o_left >= p_left and o_right <= p_right:   # player충돌rect 가 obj의 너비를 포함하는 경우
            return "top"

    # player 아랫변 충돌 검사
    if o_bottom <= p_bottom <= o_top:                 # player충돌rect 아랫변이 obj 안에 있을 때
        if o_left <= p_left <= o_right:               # player충돌rect 왼쪽이 obj 안에 있음
            return "bottom"
        if o_left <= p_right <= o_right:              # player충돌rect 오른쪽이 obj 안에 있음
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
        if o_bottom <= p_top <= o_top:     # player충돌rect 윗변이 obj 안에 있음
            return "right"
        if o_bottom <= p_bottom <= o_top:  # player충돌rect 아랫변이 obj 안에 있음
            return "right"

    return None
