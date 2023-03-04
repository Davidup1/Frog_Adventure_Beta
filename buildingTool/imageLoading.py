import pygame


def imageLoading(filename):
    imageInit = []
    for file in filename:
        print(file[0],file[1])
        img = pygame.image.load(file[0])
        imageInit.append(img)

    return imageInit