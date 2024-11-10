#! /usr/bin/env python3
''' Simple example of Pygame graphics
    Draw a sheet of notepaper with the get_at function.
'''
import pygame

def main():
    pygame.init()
    window_size_x = 400
    window_size_y = 600
    surface = pygame.display.set_mode([window_size_x,window_size_y]) 
    pygame.display.set_caption('Notepaper')
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

def draw_hard(surface, size_x, size_y):
    ''' Draw a sheet of notepaper, using nothing but pixel set functions.'''
    blue = (0, 0, 200)
    red  = (200, 0, 0)
    white = (255,255,255)
    
    # Background of the page is white
    for x in range(size_x):
        for y in range(size_y):
            surface.set_at((x,y), white)
    
    # Draw horizontal blue lines
    for y in range(60, size_y, 20):
        for x in range(size_x):
            surface.set_at((x, y), blue)
            
    # Draw one vertical red line
    x = 25
    for y in range(0, size_y):
        surface.set_at((x, y), red)
    
def draw(surface, size_x, size_y):
    ''' Draw the notepaper using line primitives.'''
    blue = (0, 0, 200)
    red  = (200, 0, 0)
    white = (255,255,255)
    
    # Background of the page is white
    surface.fill(white)
    
    # Draw horizontal blue lines
    for y in range(60, size_y, 20):
        left_side = (0, y)
        right_side = (size_x, y)
        pygame.draw.line(surface, blue, left_side, right_side)
            
    # Draw one vertical red line
    pygame.draw.line(surface, red, (25, 0), (25, size_y))

if __name__ == "__main__":
    main()