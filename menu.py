import pygame
import main as game
import sys
#code written by Connor Patterson u1408323



def text(text,font,color,surface,x,y):
    textobj = font.render(text,1,color)
    textr = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textr)



#button class setup (similarly set up to the sprite class in main)
class button:
    def __init__(self, image):
        self.image = image
        self.display_image = self.image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def draw(self, screen):
        # Same as Sprite
        screen.blit(self.image, self.rectangle)

    #customizing collision to mouse and buttons
    # def is_colliding(self): # check if colliding
    #     pos = pygame.mouse.get_pos()
    #     return pixel_collision(self.mask, self.rectangle, pos)



# Let the Menu run!
def main():
    choosing = True
    pygame.init()

    width, height = 600, 600
    size = width, height
    screen = pygame.display.set_mode((width, height))

    while choosing:
        pos = pygame.mouse.get_pos()

        M_rect = pygame.Surface((10,10))
        # M_rect.fill((0,100,100))
        M_rect_mask = pygame.mask.from_surface(M_rect)

        screen.blit(M_rect, pos)


    #button placed on screen
        Playbutton = pygame.image.load("Play button.png").convert_alpha()
        Exitbutton = pygame.image.load("Exit button.png").convert_alpha()

        play_A = pygame.transform.smoothscale(Playbutton, (100, 150))
        exit_B = pygame.transform.smoothscale(Exitbutton, (400, 150))

        play_rect = play_A.get_rect()
        play_mask = pygame.mask.from_surface(Playbutton)

        play_rect.topleft =(150,100)

        screen.blit(Playbutton,play_rect)


        exit_rect = exit_B.get_rect()
        exit_mask = pygame.mask.from_surface(Playbutton)

        exit_rect.topleft =(150,350)

        screen.blit(Exitbutton,exit_rect)


# button collision and action
        if play_mask.overlap(M_rect_mask, (pos[0] - play_rect.x, pos[1]-play_rect.y)):
            print('play')

        if exit_mask.overlap (M_rect_mask, (pos[0] - exit_rect.x, pos[1]-exit_rect.y)):
            print('exit')

    #Game Title
        myfont = pygame.font.SysFont('monospace', 24)
        text = "Avoider"
        label = myfont.render(text, True, (255, 255, 0))
        screen.blit(label, (20, 20))


    #delete to break everything \/ XP aka note to self DON'T TOUCH
        pygame.display.update()

        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        choosing = False

        pygame.time.wait(20)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()