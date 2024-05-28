import pygame

from classes.Font import Font


# Этот код определяет класс Dashboard, который представляет панель игры с информацией о состоянии игры
# (количество очков, монет, время и т.д.) и методами для её обновления и отображения

# Создание класса Dashboard, который наследуется от класса Font
class Dashboard(Font):
    def __init__(self, filePath, size, screen):
        Font.__init__(self, filePath, size)
        # Вызов конструктора родительского класса
        self.state = "menu" # Инициализация состояния панели
        self.screen = screen # Установка экрана для отображения панели
        self.levelName = "" # Название уровня
        self.points = 0
        self.coins = 0
        self.ticks = 0 # Счетчик тиков
        self.time = 0

    # Метод обновления панели
    def update(self):
        self.drawText("MARIO", 50, 20, 15) # Отображение надписи "MARIO"
        self.drawText(self.pointString(), 50, 37, 15) # Отображение количества очков

        self.drawText("@x{}".format(self.coinString()), 225, 37, 15) # Отображение количества монет

        self.drawText("WORLD", 380, 20, 15)
        self.drawText(str(self.levelName), 395, 37, 15) # Отображение названия уровня

        self.drawText("TIME", 520, 20, 15)
        if self.state != "menu": # Если не в меню
            self.drawText(self.timeString(), 535, 37, 15) # Отображение времени игры

        # обновление времени
        self.ticks += 1
        if self.ticks == 60: # Каждые 60 тиков (1 минута)
            self.ticks = 0
            self.time += 1

    # Метод отрисовки текста на панели
    def drawText(self, text, x, y, size):
        for char in text:
            charSprite = pygame.transform.scale(self.charSprites[char], (size, size)) # Масштабирование спрайта символа
            self.screen.blit(charSprite, (x, y)) # Отображение символа на экране
            if char == " ":
                x += size//2
            else:
                x += size

    # Метод для форматирования строки количества монет
    def coinString(self):
        return "{:02d}".format(self.coins)

    # Метод для форматирования строки количества очков
    def pointString(self):
        return "{:06d}".format(self.points)

    # Метод для форматирования строки времени игры
    def timeString(self):
        return "{:03d}".format(self.time)
