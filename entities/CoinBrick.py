from copy import copy

from entities.EntityBase import EntityBase
from entities.Item import Item


class CoinBrick(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, sound, dashboard, gravity=0):
        super(CoinBrick, self).__init__(x, y, gravity) # Вызов конструктора родительского класса EntityBase с передачей координат x, y и значения гравитации
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.image = self.spriteCollection.get("bricks").image # Присвоение атрибуту image изображения спрайта "bricks" из коллекции
        self.type = "Block" # Установка типа объекта на "Block"
        self.triggered = False
        self.sound = sound
        self.dashboard = dashboard
        self.item = Item(spriteCollection, screen, self.rect.x, self.rect.y) # Создание объекта Item с передачей коллекции спрайтов, экрана и координаты x, y

    def update(self, cam):
        if not self.alive or self.triggered: # Если объект не живой или затриггерился
            self.image = self.spriteCollection.get("empty").image # Установить изображение спрайта "empty"
            self.item.spawnCoin(cam, self.sound, self.dashboard) # Спавн монеты на экране
        # Отрисовка заднего фона и спрайта блока на экране с учетом позиции камеры
        self.screen.blit(
            self.spriteCollection.get("sky").image,
            (self.rect.x + cam.x, self.rect.y + 2),
        )
        self.screen.blit(self.image, (self.rect.x + cam.x, self.rect.y - 1))
