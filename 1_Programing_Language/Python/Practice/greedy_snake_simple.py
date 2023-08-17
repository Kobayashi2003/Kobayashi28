# without double buffer
import msvcrt
import win32console
import time
import random
import shutil
from enum import Enum

Direction = Enum('Direction', 'UP DOWN LEFT RIGHT')
WIDTH, HEIGHT = shutil.get_terminal_size()


def greedy_snake():

    random.seed(time.time())
    buf = win32console.CreateConsoleScreenBuffer()

    # init snake
    snake = [(WIDTH // 2, HEIGHT // 2 + i) for i in range(5)]
    direction = Direction.UP
    # init food
    food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)) 
    # draw snake
    for x, y in snake:
       buf.WriteConsoleOutputCharacter('\033[38;5;2m#\033[0m', win32console.PyCOORDType(x, y))
    # draw food
    for x, y in [food]:
       buf.WriteConsoleOutputCharacter('\033[38;5;1mO\033[0m', win32console.PyCOORDType(x, y))
    # hide cursor
    buf.SetConsoleCursorInfo(1, False)
    buf.SetConsoleActiveScreenBuffer()
    time.sleep(0.1)

    while True:
        # move snake
        tail = snake.pop()
        snake.insert(0, (snake[0][0] + (direction == Direction.RIGHT) - (direction == Direction.LEFT), 
                         snake[0][1] + (direction == Direction.DOWN) - (direction == Direction.UP)))
        # check if snake is dead
        if snake[0][0] < 0 or snake[0][0] >= WIDTH or snake[0][1] < 0 or snake[0][1] >= HEIGHT or snake[0] in snake[1:]:
            break
        # erase tail and draw head
        buf.WriteConsoleOutputCharacter(' ', win32console.PyCOORDType(tail[0], tail[1]))
        time.sleep(0.1)
        buf.WriteConsoleOutputCharacter('\033[38;5;2m#\033[0m', win32console.PyCOORDType(snake[0][0], snake[0][1]))
        
        # check if snake eats food
        if snake[0] == food:
            snake.append(tail)
            # generate new food
            food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            while food in snake:
                food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            buf.WriteConsoleOutputCharacter('\033[38;5;2m#\033[0m', win32console.PyCOORDType(tail[0], tail[1]))
            time.sleep(0.1)
            buf.WriteConsoleOutputCharacter('\033[38;5;1mO\033[0m', win32console.PyCOORDType(food[0], food[1]))

        # check if user presses a key
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'w' and direction != Direction.DOWN:
                direction = Direction.UP
            elif key == b's' and direction != Direction.UP:
                direction = Direction.DOWN
            elif key == b'a' and direction != Direction.RIGHT:
                direction = Direction.LEFT
            elif key == b'd' and direction != Direction.LEFT:
                direction = Direction.RIGHT
            elif key == b'q':
                break
        time.sleep(0.1)

    # draw end message
    end_msg = 'Game Over!'
    buf.WriteConsoleOutputCharacter(' ' * WIDTH * HEIGHT, win32console.PyCOORDType(0, 0))
    buf.WriteConsoleOutputCharacter(end_msg, win32console.PyCOORDType(WIDTH // 2 - len(end_msg) // 2, HEIGHT // 2))
    msvcrt.getch()


def main():
    greedy_snake()

if __name__ == '__main__':
    main()