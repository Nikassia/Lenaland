from copy import copy

from entities.EntityBase import EntityBase


# Определяем класс RandomBox, который является наследником класса EntityBase
class RandomBox(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, item, sound, dashboard, level, gravity=0):
        super(RandomBox, self).__init__(x, y, gravity) # Вызываем метод init родительского класса EntityBase для инициализации объекта
        # Устанавливаем значения атрибутов
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
        self.item = item
        self.level = level

    # Обновление состояния объекта
    def update(self, cam):
        if self.alive and not self.triggered: # Если объект RandomBox живой и не затриггерен, обновляем анимацию
            self.animation.update()
        else:
            # В противном случае, устанавливаем изображение анимации на пустое и выполняем действия в зависимости от типа предмета
            self.animation.image = self.spriteCollection.get("empty").image
            if self.item == 'RedMushroom':
                self.level.addRedMushroom(self.rect.y // 32 - 1, self.rect.x // 32)
                self.sound.play_sfx(self.sound.powerup_appear)
            self.item = None
            # Если время меньше максимального времени, сдвигаем объект вверх
            if self.time < self.maxTime:
                self.time += 1
                self.rect.y -= self.vel
            else:
                # В противном случае сдвигаем объект вниз
                if self.time < self.maxTime * 2:
                    self.time += 1
                    self.rect.y += self.vel
        # Отрисовываем фон неба и анимацию объекта RandomBox на экране
        self.screen.blit(
            self.spriteCollection.get("sky").image,
            (self.rect.x + cam.x, self.rect.y + 2),
        )
        self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y - 1))
