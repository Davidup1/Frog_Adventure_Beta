import pygame
import decimal


def backgroundBuilding(game):
    bgImage_list = game.bgImageInit
    fireImage_list = game.fireInit
    bg_current_frame = decimal.Decimal('0')
    fire_current_frame = decimal.Decimal('0')
    FPS_BG = decimal.Decimal('0.002')
    FPS_FIRE = decimal.Decimal('0.004')
    bg_image_list = []
    fire_image_list = []
    for image in bgImage_list:
        bg_image_list.append(image)
    for image in fireImage_list:
        fire_image_list.append(image)

    while (bg_current_frame < len(bg_image_list) or fire_current_frame < len(fire_image_list)):
        if fire_current_frame >= len(fire_image_list):
            fire_current_frame = fire_current_frame - len(fire_image_list)
        game.screen.blit(bg_image_list[int(bg_current_frame)],(0,0))
        game.screen.blit(fire_image_list[int(fire_current_frame)],(455,0))
        bg_current_frame += FPS_BG
        fire_current_frame += FPS_FIRE
        pygame.display.update()

def characterBuilding(game):
    character_img_list = game.characterInit
    FPS = decimal.Decimal('0.004')
    character_frame = decimal.Decimal('0')
    while (character_frame < len(character_img_list)):
        game.screen.blit(character_img_list[int(character_frame)],(300,100))
        character_frame += FPS
        pygame.display.update()