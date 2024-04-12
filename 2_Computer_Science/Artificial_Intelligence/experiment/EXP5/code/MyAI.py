import copy
from ChessBoard import *


class Evaluate(object):
    # 棋子棋力得分
    single_chess_point = {
        'c': 989,   # 车
        # 'm': 439,   # 马
        # 'p': 442,   # 炮
        'm': 680,
        'p':600,
        's': 226,   # 士
        'x': 210,   # 象
        'z': 55,    # 卒
        'j': 65536  # 将
    }
    # 红兵（卒）位置得分
    red_bin_pos_point = [
        [1, 3, 9, 10, 12, 10, 9, 3, 1],
        [18, 36, 56, 95, 118, 95, 56, 36, 18],
        [15, 28, 42, 73, 80, 73, 42, 28, 15],
        [13, 22, 30, 42, 52, 42, 30, 22, 13],
        [8, 17, 18, 21, 26, 21, 18, 17, 8],
        [3, 0, 7, 0, 8, 0, 7, 0, 3],
        [-1, 0, -3, 0, 3, 0, -3, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # 红车位置得分
    red_che_pos_point = [
        [185, 195, 190, 210, 220, 210, 190, 195, 185],
        [185, 203, 198, 230, 245, 230, 198, 203, 185],
        [180, 198, 190, 215, 225, 215, 190, 198, 180],
        [180, 200, 195, 220, 230, 220, 195, 200, 180],
        [180, 190, 180, 205, 225, 205, 180, 190, 180],
        [155, 185, 172, 215, 215, 215, 172, 185, 155],
        [110, 148, 135, 185, 190, 185, 135, 148, 110],
        [100, 115, 105, 140, 135, 140, 105, 115, 110],
        [115, 95, 100, 155, 115, 155, 100, 95, 115],
        [20, 120, 105, 140, 115, 150, 105, 120, 20]
    ]
    # 红马位置得分
    red_ma_pos_point = [
        [80, 105, 135, 120, 80, 120, 135, 105, 80],
        [80, 115, 200, 135, 105, 135, 200, 115, 80],
        [120, 125, 135, 150, 145, 150, 135, 125, 120],
        [105, 175, 145, 175, 150, 175, 145, 175, 105],
        [90, 135, 125, 145, 135, 145, 125, 135, 90],
        [80, 120, 135, 125, 120, 125, 135, 120, 80],
        [45, 90, 105, 190, 110, 90, 105, 90, 45],
        [80, 45, 105, 105, 80, 105, 105, 45, 80],
        [20, 45, 80, 80, -10, 80, 80, 45, 20],
        [20, -20, 20, 20, 20, 20, 20, -20, 20]
    ]
    # 红炮位置得分
    red_pao_pos_point = [
        [190, 180, 190, 70, 10, 70, 190, 180, 190],
        [70, 120, 100, 90, 150, 90, 100, 120, 70],
        [70, 90, 80, 90, 200, 90, 80, 90, 70],
        [60, 80, 60, 50, 210, 50, 60, 80, 60],
        [90, 50, 90, 70, 220, 70, 90, 50, 90],
        [120, 70, 100, 60, 230, 60, 100, 70, 120],
        [10, 30, 10, 30, 120, 30, 10, 30, 10],
        [30, -20, 30, 20, 200, 20, 30, -20, 30],
        [30, 10, 30, 30, -10, 30, 30, 10, 30],
        [20, 20, 20, 20, -10, 20, 20, 20, 20]
    ]
    # 红将位置得分
    red_jiang_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9750, 9800, 9750, 0, 0, 0],
        [0, 0, 0, 9900, 9900, 9900, 0, 0, 0],
        [0, 0, 0, 10000, 10000, 10000, 0, 0, 0],
    ]
    # 红相或士位置得分
    red_xiang_shi_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 60, 0, 0, 0, 60, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [80, 0, 0, 80, 90, 80, 0, 0, 80],
        [0, 0, 0, 0, 0, 120, 0, 0, 0],
        [0, 0, 70, 100, 0, 100, 70, 0, 0],
    ]

    red_pos_point = {
        'z': red_bin_pos_point,
        'm': red_ma_pos_point,
        'c': red_che_pos_point,
        'j': red_jiang_pos_point,
        'p': red_pao_pos_point,
        'x': red_xiang_shi_pos_point,
        's': red_xiang_shi_pos_point
    }

    def __init__(self, team):
        self.team = team

    def get_single_chess_point(self, chess: Chess):
        if chess.team == self.team:
            return self.single_chess_point[chess.name]
        else:
            return -1 * self.single_chess_point[chess.name]

    def get_chess_pos_point(self, chess: Chess):
        red_pos_point_table = self.red_pos_point[chess.name]
        if chess.team == 'r':
            pos_point = red_pos_point_table[chess.row][chess.col]
        else:
            pos_point = red_pos_point_table[9 - chess.row][chess.col]
        if chess.team != self.team:
            pos_point *= -1
        return pos_point

    def evaluate(self, chessboard: ChessBoard):
        point = 0
        for chess in chessboard.get_chess():
            point += self.get_single_chess_point(chess)
            point += self.get_chess_pos_point(chess)
        return point


class ChessMap(object):
    def __init__(self, chessboard: ChessBoard):
        self.chess_map = copy.deepcopy(chessboard.chessboard_map)


class ChessAI(object):
    def __init__(self, computer_team):
        self.team = computer_team
        self.evaluate_class = Evaluate(self.team)
        self.last_step = float('inf')

    def alpha_beta(self, chessboard: ChessBoard, depth, alpha, beta, is_max):

        # This Alpha-Beta pruning algorithm is based on recursion. 
        # The termination condition of the recursion is to reach the specified depth or the leaf node.
        # Due to the diversity of chess moves, we cannot discuss all cases of the subsequent moves of the current situation at once,
        # so we often need to artificially specify the depth to prevent the algorithm space from being too large.

        # if reach the leaf node, then return the evaluate value
        if depth == 0:
            return self.evaluate_class.evaluate(chessboard)

        if is_max:
            max_eval = -float('inf')
            count_child = 0
            for chess in chessboard.get_chess():
                    
                if chess.team != self.team:
                    continue

                put_down_position = chessboard.get_put_down_position(chess)
                count_child += len(put_down_position)

                for pos in put_down_position:
                    # save the old position and old chess on the new position 
                    old_row, old_col = chess.row, chess.col
                    chess_bak = chessboard.chessboard_map[pos[0]][pos[1]]
                    # move the current chess to the new position 
                    chess.row, chess.col = pos[0], pos[1]
                    chessboard.chessboard_map[old_row][old_col] = None
                    chessboard.chessboard_map[pos[0]][pos[1]] = chess

                    eval = self.alpha_beta(chessboard, depth - 1, alpha, beta, False)

                    # restore the old position and old chess on the new position
                    chess.row, chess.col = old_row, old_col
                    chessboard.chessboard_map[old_row][old_col] = chess
                    chessboard.chessboard_map[pos[0]][pos[1]] = chess_bak

                    # udpate the alpha value of the max node 
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    # if alpha is greater than beta, then cut the branch
                    if beta <= alpha:
                        break
            # if count_child is 0, it means that there is no valid move for the current player, 
            # so we need to evaluate the current situation
            return max_eval if count_child > 0 else self.evaluate_class.evaluate(chessboard=chessboard)
        else:
            min_eval = float('inf')
            count_child = 0
            for chess in chessboard.get_chess():

                if chess.team == self.team:
                    continue

                put_down_position = chessboard.get_put_down_position(chess)
                count_child += len(put_down_position)

                for pos in put_down_position:
                    # save the old position and old chess on the new position
                    old_row, old_col = chess.row, chess.col
                    chess_bak = chessboard.chessboard_map[pos[0]][pos[1]]
                    # move the current chess to the new position
                    chess.row, chess.col = pos[0], pos[1]
                    chessboard.chessboard_map[old_row][old_col] = None
                    chessboard.chessboard_map[pos[0]][pos[1]] = chess

                    eval = self.alpha_beta(chessboard, depth - 1, alpha, beta, True)

                    # restore the old position and old chess on the new position
                    chess.row, chess.col = old_row, old_col
                    chessboard.chessboard_map[old_row][old_col] = chess
                    chessboard.chessboard_map[pos[0]][pos[1]] = chess_bak
                    # update the beta value of the min node
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    # if beta <= alpha, then cut the branch
                    if beta <= alpha:
                        break
            # if count_child is 0, it means that there is no valid move for the current player, 
            # so we need to evaluate the current situation
            return min_eval if count_child > 0 else self.evaluate_class.evaluate(chessboard=chessboard)

    def get_next_step(self, chessboard: ChessBoard):


        import time
        import random
        from concurrent import futures

        random.seed(time.time())

        import sqlite3 

        conn = sqlite3.connect('chess.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS chess (chessboard TEXT PRIMARY KEY, old_row INTEGER, old_col INTEGER, new_row INTEGER, new_col INTEGER)')
        conn.commit()
        chessboard_str = str(self.team) + ':' + ' '.join(' '.join(row) for row in chessboard.get_chessboard_str_map())
        cursor.execute('SELECT * FROM chess WHERE chessboard = ?', (chessboard_str,))
        value = cursor.fetchone()
        if value:
            return value[1], value[2], value[3], value[4]

        
        max_eval = -float('inf')
        next_step = None

        chesses_board_list = []
        old_pos_list = []
        new_pos_list = []

        # list all the situations of the next step on the chessboard,
        # and store the old pos, new pos and the chessboard situation
        chesses = chessboard.get_chess()
        for chess in chesses:

            if chess.team != self.team:
                continue

            for pos in chessboard.get_put_down_position(chess):

                old_pos_list.append((chess.row, chess.col))
                new_pos_list.append((pos[0], pos[1]))

                chessboard_copy = ChessBoard(None)
                chessboard_copy.set_chessboard_str_map(chessboard.get_chessboard_str_map()) 

                chessboard_copy.chessboard_map[chess.row][chess.col] = None
                chessboard_copy.chessboard_map[pos[0]][pos[1]] = Chess(None, chess.team + '_' + chess.name, pos[0], pos[1])

                # remove all proterties related to pygame module,
                # to avoid objects being unable to pikcal
                chessboard_copy.image = None
                for row in chessboard_copy.chessboard_map:
                    for c in row:
                        if c:
                            c.image = None

                chesses_board_list.append(chessboard_copy)

        # create a process pool to calculate the evaluate value of each situation
        with futures.ProcessPoolExecutor(max_workers=32) as executor:
        
            if len(chesses) <= 8:
                layer = 5
            elif len(chesses) <= 24:
                layer = 4
            else:
                layer = 2

            future_to_chessboard = {executor.submit(
                self.alpha_beta, chessboard_copy, layer, -float('inf'), float('inf'), False)
                : chessboard_copy for chessboard_copy in chesses_board_list}

            for future in futures.as_completed(future_to_chessboard):
                chessboard_copy = future_to_chessboard[future]
                try:
                    eval = future.result()
                    eval = eval * random.uniform(0.8, 1.2)
                    if eval > max_eval:
                        max_eval = eval
                        index = chesses_board_list.index(chessboard_copy)
                        next_step = (*old_pos_list[index], *new_pos_list[index])
                except Exception as exc:
                    print('generated an exception: %s' % exc)
                
        cursor.execute('INSERT INTO chess VALUES (?, ?, ?, ?, ?)', (chessboard_str, *next_step))
        conn.commit()

        return next_step
