#! /usr/bin/env python3
''' Simple example of Pygame graphics
    Draw Mario into the background.  
'''
import pygame
from pathlib import Path

def main():
    WINDOW_WIDTH  = 1200
    WINDOW_HEIGHT = 622

    # Ensure all assets are accessed in an OS independent way
    # Never hardcode a filename!
    current_directory = Path('.')
    background_image = current_directory / 'assets' / 'mario_background.png'
    sprites_image    = current_directory / 'assets' / 'mario_sprites.png'

    pygame.init()
    surface = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
    pygame.display.set_caption('Mario Blit Example')
    background = pygame.image.load(background_image).convert()
    mario = pygame.image.load(sprites_image).convert()
    
    white = mario.get_at((0,0))
    mario.set_colorkey(white)
    jump_r = pygame.Rect(254, 13, 42, 49)  # source Rect to draw
    events_controller = Controller()
    
    while events_controller.running:
        events_controller.check_events()
        if not events_controller.running:
            break
        surface.blit(background, (0,0))
        surface.blit(mario, (390, 510), jump_r)
        pygame.display.flip()

class Controller:

    def __init__(self):
        self.running = True
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    self.running = False

if __name__ == "__main__":
    main()