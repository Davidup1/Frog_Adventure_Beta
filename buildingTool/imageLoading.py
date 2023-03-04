import pygame


def imageLoading(filename):
    imageInit = []
    for file in filename:
        img = pygame.image.load(file)
        imageInit.append(img)

    return imageInit