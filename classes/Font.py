from classes.Spritesheet import Spritesheet
import pygame


 # Этот код определяет класс `Font`, который представляет шрифт для отображения текста в игре
 # Класс наследуется от класса `Spritesheet` и содержит методы для загрузки спрайтов символов шрифта из изображения

# Создание класса Font, который наследуется от класса Spritesheet
class Font(Spritesheet):
    def __init__(self, filePath, size):
        Spritesheet.__init__(self, filename=filePath) # Вызов конструктора родительского класса Spritesheet
        # Список символов для создания шрифта
        self.chars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        self.charSprites = self.loadFont() # Загрузка спрайтов символов

    # Метод для загрузки спрайтов символов шрифта
    def loadFont(self):
        font = {} # Словарь для хранения спрайтов символов
        row = 0 # Номер строки в изображении со спрайтами
        charAt = 0 # Позиция символа в строке

        for char in self.chars:
            if charAt == 16: # Если достигнут конец строки спрайтов
                charAt = 0
                row += 1
            # Добавление спрайта символа в словарь font
            font.update(
                {
                    char: self.image_at(
                        charAt,
                        row,
                        2,
                        colorkey=pygame.color.Color(0, 0, 0),
                        xTileSize=8,
                        yTileSize=8
                    )
                }
            )
            charAt += 1
        return font # Возврат словаря со спрайтами символов шрифта
