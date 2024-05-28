from copy import copy

from entities.EntityBase import EntityBase


# Этот код определяет класс Coin, который представляет монету в игровом мире. Класс наследуется от класса EntityBase и имеет методы init и update.
# Метод init инициализирует атрибуты объекта, такие как экран, коллекция спрайтов и анимация монеты. Метод update обновляет состояние объекта и отображает его на экране.

class Coin(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, gravity=0):
        super(Coin, self).__init__(x, y, gravity) ## Вызов метода init родительского класса EntityBase с параметрами x, y и gravity
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.animation = copy(self.spriteCollection.get("coin").animation) ## Присвоение атрибуту animation копии анимации спрайта "coin" из коллекции спрайтов
        self.type = "Item"

    def update(self, cam):
        if self.alive:
            self.animation.update() # Обновление состояния анимации объекта
            self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y)) # Отображение изображения анимации объекта на экране с учетом позиции камеры
