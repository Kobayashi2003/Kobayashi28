#! /usr/bin/env python3
''' A template for pygame stuff '''
import pygame
from pathlib import Path

def main():
    WINDOW_WIDTH  = 400
    WINDOW_HEIGHT = 600
    
    # Ensure all assets are accessed in an OS independent way
    # Never hardcode a filename!
    current_directory = Path('.')
    background_image = current_directory / 'assets' / 'background_filename.png'
        
    pygame.init()
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('This text is at the top of your window')

    background = pygame.image.load(background_image).convert()
    surface.blit(background, (0,0))

    events    = Controller()
    
    # Create sprites here, at least for the long-term ones
            
    clock = pygame.time.Clock()  
    while events.running:
        clock.tick(60)
        events.check_events()

        if not events.running:
            break
        
        # Do other stuff
        # Update all your sprites
        if events.click:        
            mario = Mario(click, sprites_surf)
            mario_group.add(mario)

        mario_group.update(window_size_y)
        pygame.sprite.groupcollide(mario_group, coins_group, False, True)
        
        # Draw the frame here
        surface.blit(background, (0,0))
        mario_group.draw(surface)
        coins_group.draw(surface)
        pygame.display.flip()

class Mario(pygame.sprite.Sprite):

    def __init__(self, pos, sprites_surf):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((29,47))        
        self.image.blit(sprites_surf, (0,0), (4, 13, 29, 47))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=pos) 
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, size_y):
        self.rect.move_ip(0,1)
        if self.rect.top > size_y:
            self.kill()

class Controller:

    def __init__(self):
        self.left    = False
        self.right   = False
        self.running = True
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    self.left = True
                if event.key == pygame.K_RIGHT:
                    self.right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = False
                if event.key == pygame.K_RIGHT:
                    self.right = False
        if self.left and self.right:
            self.left = self.right = False

if __name__ == "__main__":
    main()