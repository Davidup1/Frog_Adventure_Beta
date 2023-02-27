import pygame
from buildingTool.imageLoading import imageLoading


class Game():
    def __init__(self):
        filename = './image/sky.jpg'
        pygame.init()
        screen = pygame.display.set_mode((800,800))
        imageLoading(screen,filename,(0,0))

        pygame.quit()

if __name__ == "__main__":
    game = Game()