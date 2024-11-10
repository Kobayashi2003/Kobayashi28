#! /usr/bin/env python3
''' Simple example of Pygame graphics
    Draw a checkerboard pattern.
'''
import pygame

def main():
    pygame.init()
    window_size_x = 405
    window_size_y = 405
    surface = pygame.display.set_mode([window_size_x,window_size_y]) 
    pygame.display.set_caption('Checkers')
    while True:
        quit = check_events()
        if quit:
            break
        draw(surface, window_size_x, window_size_y)
        pygame.display.flip()

def check_events():
    ''' A controller of sorts.  Looks for Quit type events.  
    '''
    quit = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True                
                
    return quit
    
def draw(surface, size_x, size_y):
    red   = (255, 0, 0)
    grey  = (100, 100, 100)
    black = (0, 0, 0)
    white = (255, 255, 255)
    
    # Background of the page is gray
    surface.fill(grey)
    
    box_size = size_x // 9
    strip_size = box_size // 9
    rows_with_pieces = [0, 1, 2, 5, 6, 7]
    deflate = -strip_size * 3
    
    rect = pygame.Rect(strip_size, strip_size, box_size, box_size)
    color = black
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(surface, color, rect)
            if row in rows_with_pieces and color == black:
                circle_rect = rect.inflate(deflate, deflate)
                pygame.draw.ellipse(surface, white, circle_rect)
            rect.move_ip(box_size + strip_size, 0)
            if color == black:
                color = red
            else:
                color = black
        rect.move_ip(-8*(box_size + strip_size), box_size + strip_size)
        if color == black:
            color = red
        else:
            color = black

if __name__ == "__main__":
    main()