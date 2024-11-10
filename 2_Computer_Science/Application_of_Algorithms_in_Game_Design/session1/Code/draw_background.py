#! /usr/bin/env python3
''' Simple example of Pygame graphics
    Draw the Mario background into the window.
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

    pygame.init()
    surface = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
    pygame.display.set_caption('Mario Background')
    background = pygame.image.load(background_image).convert()
    controller = Controller()
    while controller.running:
        controller.check_events()
        if not controller.running:
            break
        surface.blit(background, (0,0) )
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