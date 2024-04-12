import sys
import threading

from Game import *
from Dot import *
from ChessBoard import *
from ChessAI import *
from MyAI import ChessAI as MyAI


def ai_action(game, ai):

    if not game.get_player() == ai.team:
        return
    if game.show_win or game.show_draw:
        return

    screen = game.screen
    chessboard = game.chessboard
    chessboard_copy = ChessBoard(None)
    chessboard_copy.set_chessboard_str_map(chessboard.get_chessboard_str_map())

    cur_row, cur_col, nxt_row, nxt_col = ai.get_next_step(chessboard_copy)
    ClickBox(screen, cur_row, cur_col)
    chessboard.move_chess(nxt_row, nxt_col)
    ClickBox.clean()

    if chessboard.judge_attack_general(game.get_player()):
        if chessboard.judge_win(game.get_player()):
            print(f"{game.get_player()} win")
            game.set_win(game.get_player())
        else:
            game.set_attack(True)
    else:
        if chessboard.judge_win(game.get_player()):
            print(f"{game.get_player()} win")
            game.set_win(game.get_player())
        game.set_attack(False)

    if chessboard.judge_draw():
        print("draw")
        game.set_draw()

    game.exchange()


def main():
    background_img = pygame.image.load("images/bg.jpg")

    pygame.init()
    screen = pygame.display.set_mode((750, 667))
    chessboard = ChessBoard(screen=screen)
    game = Game(screen=screen, chessboard=chessboard)

    te_ai = ChessAI(game.user_team)
    my_ai = MyAI(game.computer_team)
    # te_ai = ChessAI(game.computer_team)
    # my_ai = MyAI(game.user_team)

    clock = pygame.time.Clock()

    ai_action_thread = None

    while True:

        if not game.show_win and not game.show_draw and game.AI_mode:
            if ai_action_thread is None or not ai_action_thread.is_alive():
                if game.get_player() == my_ai.team:
                    ai_action_thread = threading.Thread(target=ai_action, args=(game, my_ai))
                elif game.get_player() == te_ai.team:
                    ai_action_thread = threading.Thread(target=ai_action, args=(game, te_ai))
                ai_action_thread.start()

        screen.blit(background_img, (0, 0))
        screen.blit(background_img, (0, 270))
        screen.blit(background_img, (0, 540))
        chessboard.show_chessboard_and_chess()
        game.show()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                if ai_action_thread is not None:
                    ai_action_thread.join()
                sys.exit()
        
        clock.tick(60)


if __name__ == '__main__':
    main()