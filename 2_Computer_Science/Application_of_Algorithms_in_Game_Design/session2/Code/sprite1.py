#! /usr/bin/env python3
''' An example of sprites: Mario is a sprite '''
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
    pygame.display.set_caption('Mario as a Sprite')
    background = pygame.image.load(background_image).convert()
    
    mario = Mario((100, 200), sprites_image)
            
    while True:
        quit, click = check_events()
        if quit:
            break
                
        mario.update(click)
        
        surface.blit(background, (0,0))
        mario.draw(surface)
        pygame.display.flip()

class Mario(pygame.sprite.Sprite):

    def __init__(self, pos, sprites_image):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((29,47))        
        image_surf = pygame.image.load(sprites_image).convert()
        self.image.blit(image_surf, (0,0), (4, 13, 29, 47))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(topleft=pos)     
        
    def update(self, click):
        if click:
            self.rect.center = click
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

def check_events():
    ''' A controller of sorts.  Looks for Quit, several simple events.
        Returns: True/False for if a Quit event happened.
    '''
    
    quit = False
    click = None
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = event.pos
                
    return quit, click

if __name__ == "__main__":
    main()