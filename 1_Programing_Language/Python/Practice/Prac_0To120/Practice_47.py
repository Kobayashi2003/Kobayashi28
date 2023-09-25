# 假设棋盘大小为 50*50，左上角为坐标系原点(0,0)，
# 现需要写一个函数，接受两个参数，分别为方向（direction）、步长（step），该函数控制棋子的运动

origin = [0, 0]
legal_x = [0, 50]
legal_y = [0, 50]

def create(pos=origin):
    def player(direction, step):
        new_x = pos[0] + direction[0] * step
        new_y = pos[1] + direction[1] * step
        pos[0] = new_x
        pos[1] = new_y
        return pos

    return player
