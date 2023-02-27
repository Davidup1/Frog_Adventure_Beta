import pygame


def imageLoading(screen,filename,*positon):
    img = pygame.image.load(filename)
    screen.blit(img,positon)
    pygame.display.update()