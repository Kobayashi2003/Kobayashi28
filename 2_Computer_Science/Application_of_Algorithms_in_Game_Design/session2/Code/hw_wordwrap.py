#! /usr/bin/env python3
''' Starter code for HW3, problem 1 '''
import pygame
from pathlib import Path

TEXT = '''When designing a game, it is very important to provide help to the player.
Help in a game is often given by writing long instructions on the screen.
There may be better methods, however!'''

def main():
    WINDOW_WIDTH  = 1200
    WINDOW_HEIGHT = 622

    current_directory = Path('.')
    background_image = current_directory / 'assets' / 'mario_background.png'

    pygame.init()

    surface = pygame.display.set_mode([WINDOW_WIDTH,WINDOW_HEIGHT])
    pygame.display.set_caption('Mario as a Sprite')

    background = pygame.image.load(background_image).convert()
    surface.blit(background, (0,0))
    
    fontobj = setup_fonts(18)
    upper_left = (100, 30)
    length_height = (210, 500)
    wrapped_rect = pygame.Rect(upper_left, length_height)
    wrapped_surface = word_wrap(wrapped_rect, fontobj, (200, 0, 0), TEXT)
            
    while True:
        quit, click, click2 = check_events()
        if quit:
            break
        if click:
            upper_left = click
        if click2:
            length_height = ((click2[0] - upper_left[0]), (click2[1] - upper_left[1]))
            if length_height[0] > 100 and length_height[1] > 100:
                wrapped_rect = pygame.Rect(upper_left, length_height)
                wrapped_surface = word_wrap(wrapped_rect, fontobj, (200, 0, 0), TEXT)
            
        surface.blit(background, (0,0))
        surface.blit(wrapped_surface, wrapped_rect)
        pygame.draw.rect(surface, (0,0,0), wrapped_rect, width=1)
        pygame.display.flip()

def word_wrap(rect, font, text, color):
    ''' Wrap the text into the space of the rect, using the font object provided.
        Returns a surface of rect size with the text rendered in it.
    '''
    pass
    
    
def setup_fonts(font_size, bold=False, italic=False):
    ''' Load a font, given a list of preferences

        The preference list is a sorted list of strings (should probably be a parameter),
        provided in a form from the FontBook list. 
        Any available font that starts with the same letters (lowercased, spaces removed) 
        as a font in the font_preferences list will be loaded.
        If no font can be found from the preferences list, the pygame default will be returned.

        returns -- A Font object
    '''
    font_preferences = ['Helvetica Neue', 'Iosevka Regular', 'Comic Sans', 'Courier New']
    available = pygame.font.get_fonts()
    prefs = [x.lower().replace(' ', '') for x in font_preferences]
    for pref in prefs:
        a = [x
             for x in available
             if x.startswith(pref)
            ]
    if a:
        fonts = ','.join(a) #SysFont expects a string with font names in it
        return pygame.font.SysFont(fonts, font_size, bold, italic)
    return pygame.font.SysFont(None, font_size, bold, italic)
    
def check_events():
    ''' A controller of sorts.  Looks for Quit, several simple events.
        Returns: True/False for if a Quit event happened.
    '''
    
    quit = False
    click1 = click2 = None
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click1 = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            click2 = event.pos
                
    return quit, click1, click2

if __name__ == "__main__":
    main()