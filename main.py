import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario


windowSize = 640, 480


def main():
    # Инициализация звука
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize) # создание окна
    max_frame_rate = 60 # максимальное количество кадров в секунду
    # создаем приборную панель, звук, уровень и меню
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    # отображение меню и ожидание начала игры
    while not menu.start:
        menu.update()

    mario = Mario(0, 0, level, screen, dashboard, sound)
    clock = pygame.time.Clock() # создаем объект Clock для управления FPS

    while not mario.restart:
        # установка заголовка окна с указанием FPS
        pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        if mario.pause:
            mario.pauseObj.update() # обновление объекта на паузе
        else:
            # отображение уровня, приборной панели, Марио, обновление экрана
            level.drawLevel(mario.camera)
            dashboard.update()
            mario.update()
        pygame.display.update()
        clock.tick(max_frame_rate) # управление FPS
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
