#! /usr/bin/env python3
''' Simple example of Pygame graphics
    Draw an animated mario character as he walks right and jumps.
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
    pygame.display.set_caption('Mario Walking and Jumping')

    background = pygame.image.load(background_image).convert()

    mario = Mario(10, 558, sprites_image)
    event_controller = Controller()

    clock = pygame.time.Clock()
    while event_controller.running:
        clock.tick(21)
        event_controller.check_events()
        if not event_controller.running:
            break
        surface.blit(background, (0,0))
        mario.update(event_controller.right, event_controller.jump)
        mario.draw(surface)
        pygame.display.flip()

class Mario(pygame.sprite.Sprite):

    gravity = -10
    jump = [False, False] #jump[0] is when space pressed, jump[1] is when mario is in the air
    def __init__(self, x, y, sprites_file):
        # As Marios' height varies, x, y will be measured from his lower left corner
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.state = 'None'
        self.draw_index = 0
        
        self.image = pygame.image.load(sprites_file).convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.image_rects = [pygame.Rect(  4, 13, 29, 47),
                            pygame.Rect( 38, 15, 32, 45),
                            pygame.Rect( 74, 19, 46, 41),
                            pygame.Rect(125, 15, 36, 45),
                            pygame.Rect(172, 16, 34, 46),
                            pygame.Rect(215, 17, 34, 45),
                            pygame.Rect(255, 15, 40, 45),


                            pygame.Rect(303, 15, 32, 45),
                            pygame.Rect(341, 13, 24, 47),
                            pygame.Rect(368, 15, 29, 45)
                           ]

    def update(self, right, jump):
        if self.y>=558:
            Mario.jump[1] = False
        if Mario.gravity==-10 and jump:
            Mario.jump[1] = True

        x=0


        if self.state == 'None':
            if right:

                self.state = 'Right'
                self.x += 2
            elif Mario.jump[1]:

                self.state = 'Jump'

            self.draw_index=0
        elif self.state == 'Right' and not Mario.jump[1]:
            if Mario.jump[1]:
                self.state = 'Jump'
                self.draw_index = 0
                return
            self.draw_index = (self.draw_index + 1) % 13
            x = self.draw_index
            if 0<=self.draw_index<=4:
                self.draw_index = 7
            elif 5<=self.draw_index<=7:
                self.draw_index = 8
            else:
                self.draw_index = 9

            self.x += 2
            if Mario.jump[1]:
                self.draw_index = 0
            if not Mario.jump[1] and not right:
                x=0
                self.draw_index = 0
                self.state = 'None'

        elif Mario.jump[1]:


            frames = [1, 4, 5, 10, 18, 20, 21]

            self.y += Mario.gravity
            Mario.gravity += 1
            if right:
                self.x +=4
            if Mario.gravity == 11:
                x=0
                self.draw_index = 0
                self.state = 'None'
                Mario.gravity = -10
                Mario.jump[1]=False
                return
            self.draw_index = (self.draw_index + 1) % 21
            x = self.draw_index
            if 0<=self.draw_index<=frames[0]-1:
                self.draw_index = 0
            elif frames[0]<=self.draw_index<=frames[1]-1:
                self.draw_index = 1
            elif frames[1]<=self.draw_index<=frames[2]-1:
                self.draw_index = 2
            elif frames[2]<=self.draw_index<=frames[3]-1:
                self.draw_index = 3
            elif frames[3]<=self.draw_index<=frames[4]-1:
                self.draw_index = 4
            elif frames[4]<=self.draw_index<=frames[5]-1:
                self.draw_index = 5
            else:
                self.draw_index = 6

        self.rect = self.image_rects[self.draw_index].copy()
        self.rect.bottomleft = (self.x, self.y)
        self.blit_area = self.image_rects[self.draw_index]
        self.draw_index = x

    def draw(self, target_surface):
        target_surface.blit(self.image, self.rect, area=self.blit_area)

class Controller:

    def __init__(self):
        self.left    = False
        self.right   = False
        self.jump    = False
        self.running = True
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    quit = True
                if event.key == pygame.K_LEFT:
                    self.left = True
                if event.key == pygame.K_RIGHT:
                    self.right = True
                if event.key == pygame.K_SPACE:
                    self.jump = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = False
                if event.key == pygame.K_RIGHT:
                    self.right = False
                if event.key == pygame.K_SPACE:
                    self.jump = False
                    
        if self.left and self.right:
            self.left = self.right = False

if __name__ == "__main__":
    main()