from copy import copy

from classes.Dashboard import Dashboard
from classes.Maths import Vec2D


# В этом коде инициализируются атрибуты объектов, прописываются правила спавна монеты на экране и обновления ее анимации в зависимости от таймера анимации,
# происходит изменение скорости и позиции монеты, воспроизведение звука и отображение 100 очков на экране
class Item(Dashboard):
    def __init__(self, collection, screen, x, y):
        super(Item, self).__init__("./img/font.png", 8, screen) # Вызов конструктора родительского класса Dashboard с передачей пути к изображению, размера шрифта и экрана
        self.ItemPos = Vec2D(x, y) # Создание объекта Vec2D для хранения позиции предмета.
        self.itemVel = Vec2D(0, 0) # Создание объекта Vec2D для хранения скорости предмета.
        self.screen = screen
        self.coin_animation = copy(collection.get("coin-item").animation) # Копирование анимации монеты из коллекции спрайтов.
        self.sound_played = False

    def spawnCoin(self, cam, sound, dashboard):
        if not self.sound_played: # Если звук еще не проигрывался.
            self.sound_played = True
            dashboard.points += 100 # Увеличить количество очков на панели управления на 100.
            sound.play_sfx(sound.coin) # Воспроизвести звук монеты.
        self.coin_animation.update() # Обновление анимации монеты.
        if self.coin_animation.timer < 45: # Если таймер анимации меньше 45.
            if self.coin_animation.timer < 15:
                self.itemVel.y -= 0.5 # Уменьшить скорость по оси y.
                self.ItemPos.y += self.itemVel.y # Обновить позицию предмета по оси y.
            elif self.coin_animation.timer < 45:
                self.itemVel.y += 0.5 # Увеличить скорость по оси y.
                self.ItemPos.y += self.itemVel.y # Обновить позицию предмета по оси y.
            self.screen.blit(
                self.coin_animation.image, (self.ItemPos.x + cam.x, self.ItemPos.y) # Отобразить изображение анимации монеты на экране.
            )
        elif self.coin_animation.timer < 80:
            self.itemVel.y = -0.75 # Установить отрицательную скорость по оси y.
            self.ItemPos.y += self.itemVel.y # Обновить позицию предмета по оси y.
            self.drawText("100", self.ItemPos.x + 3 + cam.x, self.ItemPos.y, 8) # Написать текст "100" на экране в указанной позиции.
