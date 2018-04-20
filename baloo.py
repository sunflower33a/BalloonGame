import pygame, sys
from pygame.locals import *
import pygame_textinput
import os
from MyFont import Peas, Orange, Slab

pygame.init()

# PREDEFINED stuff
W = 1120
H = 700
FPS = 1
# timer = pygame.time.Clock()
# timer.tick(FPS)
zero = (0, 0)
WHITE = (234, 234, 234)
SEA = (194, 242, 222)
PINK = (247, 115, 109)
BLACK = (10,10,10)
window = (W, H)
center = (W/2-100, H/2)


# FONT

# TEXT SURFACE


# IMAGE LINK
BG      = 'artwork/BG/bg-background.png'
START   = 'artwork/BG/bg-startSCREEN.png'
RULE    = 'artwork/BG/bg-ruleSCREEN.png'
WATER   = 'artwork/BG/BG-water-full.png'
LILY    = 'artwork/BG/BG-leaves-full.png'
PLAYER  = 'artwork/frog1.png'
COMPA   = 'artwork/frog2.png'
COMPB   = 'artwork/frog3.png'
COMPC   = 'artwork/frog4.png'
CUSOR   = 'artwork/cusor.png'


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (W,H))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Transparent(pygame.sprite.Sprite):
    def __init__(self, image_file, location, size):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file).convert_alpha()
        if size<1 and size>0:
            size = tuple((int(size*self.image.get_rect()[2]), int(size*self.image.get_rect()[3])))
        print size
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.center = location

class Button(pygame.sprite.Sprite):
    pass

# # SCREEN
# BackGround = Background(BG, zero)

# OBJECT
#Player = Transparent(PLAYER, )


class Scene(object):
    def __init__(self):
        self.next = self

    def Render(self, screen):
        raise NotImplementedError

    def Update(self):
        raise NotImplementedError

    def HandleEvents(self, events, pressed_key):
        raise NotImplementedError

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


class TitleScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.name_input = pygame_textinput.TextInput()
        self.input_pos = (W/2, H/2 + 10)
        self.TitleText = Peas(50).render('Enter to Start', False, (0,0,0))

    def HandleEvents(self, events, pressed_key):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(RuleScene())
        self.name_input.update(events)
        # self.name_input.clear_text()

    def Update(self):
        self.name_input.get_text()

    def Render(self, screen):
        screen.fill(WHITE)
        start_screen = Background(START, zero)
        screen.blit(start_screen.image, start_screen.rect)
        screen.blit(self.TitleText, ((W-self.TitleText.get_rect().width)/2, ((H/3)*2)))
        screen.blit(self.name_input.get_surface(), center)



class RuleScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def Render(self, screen):
        screen.fill(WHITE)
        rule_screen = Background(RULE, zero)
        screen.blit(rule_screen.image, rule_screen.rect)
        title = Orange(100).render("RULE", False, PINK)
        title_rect = title.get_rect()
        screen.blit(title, ((W-title_rect.width)/2, (H-title_rect.height)/5))

        # REDO THE BACKGROUND SO THAT THE RULE IS PRINTED IN THE BACKGROUND
        next = Slab(30).render("Enter to PLAY", False, BLACK)
        next_rect = next.get_rect()
        screen.blit(next, (int((W-next_rect.width)*7/8), int(H*4.5/7)))

    def Update(self):
        pass

    def HandleEvents(self, events, pressed_key):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.SwitchToScene(GameScene())

class GameScene(Scene):
    def __init__(self):
        Scene.__init__(self)

    def HandleEvents(self, events, pressed_key):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        # Back Ground
        screen.fill(WHITE)
        lily_img = Transparent(LILY, zero, window)
        water_img = Transparent(WATER, zero, window)
        play_screen = water_img.image.copy()
        play_screen.blit(lily_img.image, zero)
        screen.blit(play_screen, pygame.rect.Rect(0, 0, 128, 128))
        # frog1_img = Transparent(PLAYER, )
        # PLAY

        # RESULT


def run(width, height, fps, start_scene):
    screen = pygame.display.set_mode((W, H))
    active_scene = start_scene
    pygame.display.set_caption('Colonel Balloon')
    timer = pygame.time.Clock()

    while active_scene != None:
        events = pygame.event.get()
        pressed_key = pygame.key.get_pressed()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        active_scene.HandleEvents(events, pressed_key)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next
        pygame.display.update()
        timer.tick(fps)


run(W, H, 6, TitleScene())