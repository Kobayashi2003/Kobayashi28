import msvcrt
import win32console
import random
import time
import shutil 
from enum import Enum 
from io import StringIO

Direction = Enum('Direction', 'UP DOWN LEFT RIGHT')

# game board
WIDTH, HEIGHT = shutil.get_terminal_size()
# snake 
INIT_LEN = 5
SNAKE_HEAD_COLOR = (0, 0, 255)
SNAKE_BODY_COLOR = (0, 255, 0)
# food
FOOD_COLOR = (255, 0, 0)


class Buffers:

    def __init__(self, num=2):
        self.num = num
        self.buffers = [win32console.CreateConsoleScreenBuffer() for _ in range(num)]
        self.current = 0
        self.last = 0

    def switch(self):
        self.last = self.current
        self.current = (self.current + 1) % self.num
        self.buffers[self.current] = win32console.CreateConsoleScreenBuffer()

    def write(self, data):
        self.buffers[self.current].WriteConsole(data)
    
    def flush(self):
        self.buffers[self.current].SetConsoleActiveScreenBuffer()
        self.buffers[self.last].Close()


class Snake:
    def __init__(self, x, y, direction):
        self.body = [(x, y)]
        self.direction = direction
        if direction == Direction.UP:
            for i in range(1, INIT_LEN):
                self.body.append((x, y + i))
        elif direction == Direction.DOWN:
            for i in range(1, INIT_LEN):
                self.body.append((x, y - i))
        elif direction == Direction.LEFT:
            for i in range(1, INIT_LEN):
                self.body.append((x + i, y))
        elif direction == Direction.RIGHT:
            for i in range(1, INIT_LEN):
                self.body.append((x - i, y))
        
    def move(self):
        x, y = self.body[0]
        if self.direction == Direction.UP:
            y -= 1
        elif self.direction == Direction.DOWN:
            y += 1
        elif self.direction == Direction.LEFT:
            x -= 1
        elif self.direction == Direction.RIGHT:
            x += 1
        self.body.insert(0, (x, y))
        self.body.pop()
        
    def change_direction(self, direction):
        self.direction = direction

    def eat(self):
        last1 = self.body[-1]
        last2 = self.body[-2]
        if last1[0] - last2[0] == 0:
            if last1[1] > last2[1]:
                self.body.append((last1[0], last1[1] + 1))
            else:
                self.body.append((last1[0], last1[1] - 1))
        else:
            if last1[0] > last2[0]:
                self.body.append((last1[0] + 1, last1[1]))
            else:
                self.body.append((last1[0] - 1, last1[1]))


    def is_dead(self):
        x, y = self.body[0]
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False
    

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game:
    def __init__(self):
        self.snake = Snake(WIDTH // 2, HEIGHT // 2, Direction.RIGHT)
        self.food = Food(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        self.score = 0
        self.game_over = False
        self.bufs = Buffers()

    def update(self, seed=None):
        if seed:
            random.seed(seed)
        self.snake.move()
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.snake.eat()
            while (self.food.x, self.food.y) in self.snake.body:
                self.food.x = random.randint(0, WIDTH - 1)
                self.food.y = random.randint(0, HEIGHT - 1)
            self.score += 1
        if self.snake.is_dead():
            self.game_over = True

    def draw(self):
        self.bufs.switch()
        output = StringIO()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) in self.snake.body:
                    if (x, y) == self.snake.body[0]:
                        output.write('\033[38;2;{};{};{}m#\033[0m'.format(*SNAKE_HEAD_COLOR))
                    else:
                        output.write('\033[38;2;{};{};{}m#\033[0m'.format(*SNAKE_BODY_COLOR))
                elif x == self.food.x and y == self.food.y:
                    output.write('\033[38;2;{};{};{}mO\033[0m'.format(*FOOD_COLOR))
                else:
                    output.write(' ')
            if y != HEIGHT - 1:
                output.write('\n')
        output.write('\033[?25l')
        self.bufs.write(output.getvalue())
        self.bufs.flush()

    def end(self):
        self.bufs.switch()
        output = StringIO()
        output_msg1 = 'Game Over!'
        output.write('\033[{};{}H'.format(HEIGHT // 2, WIDTH // 2 - len(output_msg1) // 2))
        output.write('\033[38;2;{};{};{}m{}\033[0m'.format(*FOOD_COLOR, output_msg1))
        output.write('\n')
        output_msg2 = 'Your score is {}'.format(self.score)
        output.write('\033[{};{}H'.format(HEIGHT // 2 + 1, WIDTH // 2 - len(output_msg2) // 2))
        output.write('\033[38;2;{};{};{}m{}\033[0m'.format(*FOOD_COLOR, output_msg2))
        output.write('\033[?25h')
        self.bufs.write(output.getvalue())
        self.bufs.flush()


def main():
    game = Game()
    while not game.game_over:
        game.update(time.time())
        game.draw()
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'w':
                if game.snake.direction != Direction.DOWN:
                    game.snake.change_direction(Direction.UP)
            elif key == b's':
                if game.snake.direction != Direction.UP:
                    game.snake.change_direction(Direction.DOWN)
            elif key == b'a':
                if game.snake.direction != Direction.RIGHT:
                    game.snake.change_direction(Direction.LEFT)
            elif key == b'd':
                if game.snake.direction != Direction.LEFT:
                    game.snake.change_direction(Direction.RIGHT)
            elif key == b'q':
                break
        time.sleep(0.1)
    game.end()
    while not msvcrt.kbhit():
        pass


if __name__ == '__main__': 
    main()