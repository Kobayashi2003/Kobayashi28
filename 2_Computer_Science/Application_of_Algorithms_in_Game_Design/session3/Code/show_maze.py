#! /usr/bin/env python3
''' Show off mazes and their algorithms. '''
import pygame
import pygame.gfxdraw
from pygame.locals import *
import mazes

NUM_ROWS = 24
NUM_COLS = 32
CELL_SIZE = 32
MARGIN_ONE_SIDE = 5
MARGIN = 2 * MARGIN_ONE_SIDE
WALL_COLOR = (200,200,200)

def main():
    WINDOW_WIDTH  = NUM_COLS * CELL_SIZE + MARGIN
    WINDOW_HEIGHT = NUM_ROWS * CELL_SIZE + MARGIN
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
    pygame.display.set_caption('Maze Algorithm Demonstrator')
    running = True
    markup = None
    longestpath = False
    deadends = False
    colorize = False
    g = mazes.Grid(NUM_ROWS,NUM_COLS)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == K_q:  # Quit
                    running = False
                elif event.key == K_n:  # New
                    g = mazes.Grid(NUM_ROWS,NUM_COLS)
                    markup = None
                elif event.key == K_f:  # Save to FILE
                    pygame.image.save(screen, 'maze.png')
                elif event.key == K_b:  # Binary Tree
                    mazes.binary_tree(g)
                    markup = None
                elif event.key == K_s:  # Sidewinder
                    mazes.sidewinder(g,.5)
                    markup = None
                elif event.key == K_a:  # Aldous-Broder random walk
                    mazes.aldous_broder(g)
                    markup = None
                elif event.key == K_w:  # Wilson
                    mazes.wilson(g)
                    markup = None
                elif event.key == K_r:  # Recursive Backtracker
                    mazes.recursive_backtracker(g)
                    markup = None
                elif event.key == K_l:  # longest path
                    longestpath = not longestpath
                    if longestpath:
                        markup = mazes.LongestPathMarkup(g)
                    else:
                        markup = None
                elif event.key == K_d:  # deadend count and color
                    deadends = not deadends
                    if deadends:
                        m = mazes.Markup(g, default=0)
                        print(f'There are {len(g.deadends())} deadends')
                        for c in g.deadends():
                            m[c] = 1
                        markup = mazes.ColorizedMarkup(g)
                        markup.intensity_colorize(m)
                    else:
                        markup = None
                elif event.key == K_c:  # Colorize a Dijkstra from the center
                    colorize = not colorize
                    if colorize:
                        markup = mazes.ColorizedMarkup(g, channel='G')
                        markup.colorize_dijkstra()
                    else:
                        markup = None
        display_grid(g, markup, screen)
        pygame.display.flip()            

def pos_to_colrow(pos):
    ''' Convert a position on the screen (in pixel units) to the row/column of 
        the cell at that position.
    '''
    pos_x, pos_y = pos
    col = (pos_x - MARGIN_ONE_SIDE) // CELL_SIZE
    row = (MARGIN_ONE_SIDE) // CELL_SIZE
    return (col, row)
    
def colrow_to_pos(row, col):
    ''' Convert the row/column of a cell into the position on the screen (in
        pixel units).
        
        Note: the returned location is the origin of the cell.  That is, the
        upper left pixel of the cell.
    '''
    cell_x = col * CELL_SIZE + MARGIN_ONE_SIDE
    cell_y = row * CELL_SIZE + MARGIN_ONE_SIDE
    return (cell_x, cell_y)

def draw_horizontal_wall(screen, x, y):
    pygame.draw.line(screen, WALL_COLOR, (x,y), (x+CELL_SIZE-1, y))
    
def draw_vertical_wall(screen, x, y):
    pygame.draw.line(screen, WALL_COLOR, (x,y), (x,y+CELL_SIZE-1))
        
def display_grid(g, markup, screen):
    ''' Draw the grid, and any associated markup values, to the screen. '''
    screen.fill((0,0,0))
    for row in range(g.num_rows):
        for col in range(g.num_columns):
            c = g.cell_at(row, col)
            cell_x, cell_y = colrow_to_pos(row, col)
            if markup:
                value = markup.get_item_at(row, col)
                if not value:
                    continue
                if value == '*':  # Path marker
                    pygame.draw.circle(screen,
                                       (150,80,50),
                                       (cell_x+CELL_SIZE//2,cell_y+CELL_SIZE//2),
                                       CELL_SIZE//4 - 1,  #radius
                                       0)  #filled
                if value == '^':  # Start/end marker
                    pygame.draw.circle(screen,
                                       (250,200,75),
                                       (cell_x+CELL_SIZE//2,cell_y+CELL_SIZE//2),
                                       CELL_SIZE//4 + 1,  #radius
                                       0)  #filled
                if isinstance(value, list) and len(value) == 3: # A color
                    pygame.draw.rect(screen,
                                     value,  # color
                                     (cell_x, cell_y, CELL_SIZE, CELL_SIZE))

            if not c.north or not c.is_linked(c.north):
                draw_horizontal_wall(screen, cell_x, cell_y)
            if not c.south or not c.is_linked(c.south):
                draw_horizontal_wall(screen, cell_x, cell_y+CELL_SIZE-1)
            if not c.east or not c.is_linked(c.east):
                draw_vertical_wall(screen, cell_x+CELL_SIZE-1, cell_y)
            if not c.west or not c.is_linked(c.west):
                draw_vertical_wall(screen, cell_x, cell_y)
            
if __name__ == "__main__":
    main()