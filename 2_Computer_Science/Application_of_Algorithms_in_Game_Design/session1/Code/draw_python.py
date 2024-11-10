#! /usr/bin/env python3
''' Simple example of Pygame graphics primitives
    Draw the Python Logo.
'''
import pygame

def main():
    pygame.init()
    window_size_x = 158
    window_size_y = 160
    surface = pygame.display.set_mode([window_size_x,window_size_y]) 
    pygame.display.set_caption('Python Logo')
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
    blue    = ( 71, 116, 168)
    yellow  = (249, 220, 101)
    white   = (255, 255, 255)
    radians = 3.14159/180
    
    # Background of the page is white
    surface.fill(white)
    
    points = [(27, 50), (76, 50), (76, 45), (45, 45), (45, 26)]
    pygame.draw.lines(surface, blue, False, points)
    pygame.draw.arc(surface, blue, (45, 15, 61, 22), 0*radians, 180*radians)
    pygame.draw.line(surface, blue, (106, 26), (106, 62)) 
    pygame.draw.arc(surface, blue, (76, 47, 30, 30), 270*radians, 0*radians) 
    pygame.draw.line(surface, blue, (91, 76), (57 ,76))     
    pygame.draw.arc(surface, blue, (41, 76, 32, 32), 90*radians, 180*radians) 
    pygame.draw.line(surface, blue, (41, 91), (41, 110))
    pygame.draw.line(surface, blue, (41,110), (27, 110))
    pygame.draw.arc(surface, blue, (12,50,30, 60), 90*radians, 270*radians)
    
    # Transform to yellow
    points_p = [
                transform_point(p[0], p[1]) 
                for p in points
               ]
    pygame.draw.lines(surface, yellow, False, points_p)
    pygame.draw.arc(surface, yellow, transform_rect((45, 15, 61, 22)), 180*radians, 360*radians)
    pygame.draw.line(surface, yellow, transform_point(106, 26), transform_point(106, 63)) 
    pygame.draw.arc(surface, yellow, transform_rect((76, 47, 30, 30)), 90*radians, 180*radians) 
    pygame.draw.line(surface, yellow, transform_point(91, 76), transform_point(57 ,76))     
    pygame.draw.arc(surface, yellow, transform_rect((41, 76, 32, 32)), 270*radians, 360*radians) 
    pygame.draw.line(surface, yellow, transform_point(41, 91), transform_point(41, 110))
    pygame.draw.line(surface, yellow, transform_point(41,110), transform_point(27, 110))
    pygame.draw.arc(surface, yellow, transform_rect((12,50,30, 60)), 270*radians, 90*radians)
    
    fill(surface, size_x, size_y, blue)
    fill(surface, size_x, size_y, yellow)
    
    pygame.draw.circle(surface, white, (60, 32), 7)
    pygame.draw.circle(surface, white, transform_point(60, 32), 7)
        
def transform_rect(rect):
    x, y, width, height = rect
    return (158-x-width, 160-y-height, width, height)
    
def transform_point(x, y):
    return (158-x, 160-y)
    
def fill(surface, size_x, size_y, line_color):
    ''' Blue and Yellow outlines are already drawn.  Fill them in. '''
    
    for y in range(size_y):
        first = 0
        while first < size_x:
            color = surface.get_at((first, y))
            if color != line_color:
                first += 1
            else:
                break
        last = size_x - 1
        while last > first:
            color = surface.get_at((last, y))
            if color != line_color:
                last -= 1
            else:
                break
                
        if first >= last:  # line had none of the line_color
            continue
            
        pygame.draw.line(surface, line_color, (first, y), (last, y))
        
if __name__ == "__main__":
    main()