from copy import copy

from entities.EntityBase import EntityBase
from entities.Item import Item


# В данном коде реализован класс CoinBox, представляющий объект монетного блока в игре, с методами для обновления его состояния, отрисовки на экране и других действий в зависимости от текущего состояния объекта

# Определяем класс CoinBox, который является наследником класса EntityBase
class CoinBox(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, sound, dashboard, gravity=0):
        super(CoinBox, self).__init__(x, y, gravity) # Вызываем метод init родительского класса EntityBase для инициализации объекта
        # Устанавливаем значения атрибутов объекта
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.animation = copy(self.spriteCollection.get("CoinBox").animation)
        self.type = "Block"
        self.triggered = False
        self.time = 0
        self.maxTime = 10
        self.sound = sound
        self.dashboard = dashboard
        self.vel = 1
        self.item = Item(spriteCollection, screen, self.rect.x, self.rect.y)

    # Обновляем состояние объекта в зависимости от текущего состояния
    def update(self, cam):
        # Если объект CoinBox живой и не активирован, обновляем анимацию
        if self.alive and not self.triggered:
            self.animation.update()
        else:
            # В противном случае, устанавливаем изображение анимации на пустое и спавним монету
            self.animation.image = self.spriteCollection.get("empty").image
            self.item.spawnCoin(cam, self.sound, self.dashboard)
            # Сдвигаем объект вверх
            if self.time < self.maxTime:
                self.time += 1
                self.rect.y -= self.vel
            else:
                # Сдвигаем объект вниз
                if self.time < self.maxTime * 2:
                    self.time += 1
                    self.rect.y += self.vel
        # Отрисовка фона неба и анимации объекта на экране
        self.screen.blit(
            self.spriteCollection.get("sky").image,
            (self.rect.x + cam.x, self.rect.y + 2),
        )
        self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y - 1))
