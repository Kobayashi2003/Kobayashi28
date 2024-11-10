#! /usr/bin/env python3
''' A simple pygame intro example '''
import pygame

def main():
    pygame.init()
    
    size = width, height = 1024, 768
    speed = [3,2]
    black = (0, 0, 0)
    white = (255,255,255)
    
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Text Bouncer')
    font = setup_fonts(48)

    while True:
        text = input('What would you like to say? ')
        text_surface = font.render(text, True, white, black)    
        text_width, text_height = text_surface.get_size()
        if text_width < width * .8:
            break
        print('You are too wordy. Try again.')
    text_x = text_y = 0
    
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        text_x += speed[0]
        text_y += speed[1]
        
        if text_x < 0 or text_x + text_width > width:
            speed[0] = -speed[0]
        if text_y < 0 or text_y + text_height > height:
            speed[1] = -speed[1]
        
        screen.fill(black)
        screen.blit(text_surface, (text_x, text_y))
        pygame.display.flip()
    
def setup_fonts(font_size, bold=False, italic=False):
    ''' Load a font, given a list of preferences

        The preference list is a sorted list of strings (should probably be a parameter),
        provided in a form from the FontBook list. 
        Any available font that starts with the same letters (lowercased, spaces removed) 
        as a font in the font_preferences list will be loaded.
        If no font can be found from the preferences list, the pygame default will be returned.

        returns -- A Font object
    '''
    font_preferences = ['Bangers', 'Iosevka Regular', 'Comic Sans', 'Courier New']
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

if __name__ == "__main__":
    main()