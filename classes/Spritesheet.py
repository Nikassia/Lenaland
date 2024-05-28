import pygame


# Этот код определяет класс Spritesheet, который предназначен для работы с изображениями спрайтов
# Он позволяет извлекать спрайты из изображения и масштабировать их по заданным параметрам

class Spritesheet(object):
    # Инициализация класса с загрузкой изображения
    def __init__(self, filename):
        try:
            # Загрузка изображения из файла
            self.sheet = pygame.image.load(filename)
            self.sheet = pygame.image.load(filename)
            if not self.sheet.get_alpha():
                self.sheet.set_colorkey((0, 0, 0)) # Установка цвета прозрачности
        except pygame.error:
            print("Unable to load spritesheet image:", filename)
            raise SystemExit

    # Метод для извлечения спрайта из изображения по заданным координатам
    def image_at(self, x, y, scalingfactor, colorkey=None, ignoreTileSize=False,
                 xTileSize=16, yTileSize=16):
        if ignoreTileSize:
            rect = pygame.Rect((x, y, xTileSize, yTileSize))
        else:
            rect = pygame.Rect((x * xTileSize, y * yTileSize, xTileSize, yTileSize))
        # Создание поверхности для спрайта
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect) # Создание поверхности для спрайта
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL) # Установка цвета прозрачности
        return pygame.transform.scale(
            image, (xTileSize * scalingfactor, yTileSize * scalingfactor)
        ) # Масштабирование спрайта до указанного масштабного коэффициента
