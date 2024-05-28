import random

from classes.Collider import Collider


class LeftRightWalkTrait:
    def __init__(self, entity, level):
        self.direction = random.choice([-1, 1]) # Выбираем случайное направление (-1 или 1) для движения.
        self.entity = entity
        self.collDetection = Collider(self.entity, level)
        self.speed = 1 # Устанавливаем скорость движения
        self.entity.vel.x = self.speed * self.direction # Устанавливаем скорость движения по оси x.

    def update(self):
        if self.entity.vel.x == 0: # Если скорость по оси x равна 0
            self.direction *= -1 # Меняем направление движения.
        self.entity.vel.x = self.speed * self.direction # Устанавливаем скорость движения по оси x с учетом направления.
        self.moveEntity() # Вызываем метод для перемещения объекта.

    def moveEntity(self):
        self.entity.rect.y += self.entity.vel.y # Обновляем позицию объекта по оси y.
        self.collDetection.checkY() # Проверяем столкновения по оси y.
        self.entity.rect.x += self.entity.vel.x # Обновляем позицию объекта по оси x.
        self.collDetection.checkX() # Проверяем столкновения по оси x.
