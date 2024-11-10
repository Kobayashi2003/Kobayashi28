#! /usr/bin/env python3
''' Play a simple drop game '''
import sys, random
import pygame
import pygame.locals
import pygame.time

WINDOW_WIDTH  = 400
WINDOW_HEIGHT = 600
REDBOX_WIDTH  =  10
REDBOX_HEIGHT =  25

class Platform:
    ''' Platforms start from the bottom of the screen and move up.  Each
        has a gap through which the Avatar can fall.
    '''
    
    # Class variables!
    delay = 2000         # New platform starts up every 2000 microseconds
    fastest_delay = 700  # and decreases until they are coming every 700 mseconds
    time_of_last_platform = 0
    THICKNESS = 10
    GAP_WIDTH = 40
    speed = 3
    
    def __init__(self):
        self.y = WINDOW_HEIGHT
        self.gap_x = random.randint(0, WINDOW_WIDTH - Platform.GAP_WIDTH)
        Platform.time_of_last_platform = pygame.time.get_ticks()
        Platform.delay = max(Platform.fastest_delay, Platform.delay - 50)
        
    def collision(self, avatar_x, avatar_y, avatar_width):
        ''' Return True if the avatar would be drawn within the solid portion
            of this platform.
        '''
        assert avatar_x >= 0
        assert avatar_x < WINDOW_WIDTH
        assert avatar_y >= 0
        assert avatar_y < WINDOW_HEIGHT
        if avatar_y < self.y or avatar_y > self.y + Platform.THICKNESS:
            return False
        # If avatar is over the gap, then no collision
        if avatar_x < self.gap_x:
            return True
        if avatar_x + avatar_width > self.gap_x + Platform.GAP_WIDTH:
            return True
        return False
        
    def update(self):
        ''' Platform just needs to move up with each update.
        
            Returns: False when the platform's bottom is no longer viewable.
        '''
        self.y -= Platform.speed
        return self.y > -Platform.THICKNESS
        
    def draw(self, surface):
        ''' Draw the platform.
        '''
        pygame.draw.rect(surface,  # draw the platform in white
                         (255,255,255),
                         (0,self.y,WINDOW_WIDTH,Platform.THICKNESS)
                        )
        pygame.draw.rect(surface,  # draw the gap in black
                         (0,0,0),
                         (self.gap_x, self.y, Platform.GAP_WIDTH, Platform.THICKNESS)
                        )


pygame.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Drop!')

platforms = []

   
redbox_x = WINDOW_WIDTH/2-REDBOX_WIDTH/2
redbox_y = 1
redbox_vx = 5
redbox_vy = 3
left_down = False
right_down = False
start_time = pygame.time.get_ticks()
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(30)
    surface.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_down = True
            if event.key == pygame.K_RIGHT:
                right_down = True
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_down = False
            if event.key == pygame.K_RIGHT:
                right_down = False
    if left_down and right_down:
        left_down = False
        right_down = False
        
    done_platform = False
    for platform in platforms:
        if not platform.update():
            done_platform = platform
        platform.draw(surface)
    if done_platform:
        platforms.remove(done_platform)
        
    if pygame.time.get_ticks() - Platform.time_of_last_platform > Platform.delay:
        new_platform = Platform()
        platforms.append(new_platform)
        
    # Update the player's avatar position
    if left_down:
        redbox_x = max(0, redbox_x-redbox_vx)
    if right_down:
        redbox_x = min(redbox_x+redbox_vx, WINDOW_WIDTH-REDBOX_WIDTH)
    
    #update y: Check to see if riding a platform, if so then y is decremented
    #          else, fall
    bottom_left_y = redbox_y + REDBOX_HEIGHT - 1
    riding = None
    for platform in platforms:
        if platform.collision(redbox_x, bottom_left_y, REDBOX_WIDTH):
            riding = platform
            break
    if riding:
        bottom_left_y = riding.y
        redbox_y = bottom_left_y - REDBOX_HEIGHT        
    else:
        redbox_y += redbox_vy
    
    if redbox_y < 0:
        break
        
    if redbox_y + REDBOX_HEIGHT > WINDOW_HEIGHT:
        break
    
    # Draw the player's avatar
    pygame.draw.rect(surface, (255,0,0), (redbox_x, redbox_y, REDBOX_WIDTH, REDBOX_HEIGHT))

    pygame.display.update()
score = (pygame.time.get_ticks() - start_time)/1000
print(f'You survived for {score} seconds')
    
        
                        

                            
