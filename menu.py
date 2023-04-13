import pygame
import main as game
import sys
#code written by Connor Patterson u1408323



def text(text,font,color,surface,x,y):
    textobj = font.render(text,1,color)
    textr = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textr)





def main_menu(screen):
    Choosing=True
    while Choosing:

        #Mouse positions
        mouse_X, mouse_Y = pygame.mouse.get_pos()

        #menu buttons
        Play_button = pygame.Rect(40,100,100,40)
        Exit_button = pygame.Rect(40,300,100,40)

        # selecting detection
        if Play_button.collidepoint((mouse_X,mouse_Y)):
            pass

        #leaving the game buttons
        if Exit_button.collidepoint((mouse_X,mouse_Y)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Choosing = False

                    pygame.time.wait(20)
                    pygame.quit()
                    sys.exit()

        #drawing buttons
        pygame.draw.rect(screen, (255,0,0),Play_button)
        pygame.draw.rect(screen, (255, 0, 0), Exit_button)

        # click = false






def main():
    pygame.init()
    width, height = 600, 600
    size = width, height
    screen = pygame.display.set_mode((width, height))


    myfont = pygame.font.SysFont('monospace', 24)
    text = "Avoider"
    label = myfont.render(text, True, (255, 255, 0))
    screen.blit(label, (20, 20))


    main_menu(screen)

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         is_playing = False

    pygame.display.update()
    pygame.time.wait(20)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()