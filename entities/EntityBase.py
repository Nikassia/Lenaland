import pygame

from classes.Maths import Vec2D


class EntityBase(object):
    def __init__(self, x, y, gravity):
        self.vel = Vec2D() # # Создание атрибута vel, являющегося экземпляром класса Vec2D
        self.rect = pygame.Rect(x * 32, y * 32, 32, 32) # # Создание атрибута rect, являющегося прямоугольником с координатами x и y, шириной и высотой 32 пикселя
        self.gravity = gravity
        self.traits = None
        self.alive = True
        self.active = True
        self.bouncing = False
        self.timeAfterDeath = 5
        self.timer = 0
        self.type = ""
        self.onGround = False
        self.obeyGravity = True
        
    def applyGravity(self):
        if self.obeyGravity: # Проверка, если объект должен подчиняться гравитации
            self.vel.y += self.gravity # Увеличение вертикальной скорости объекта на значение гравитации

    def updateTraits(self):
        for trait in self.traits.values():
            try:
                trait.update() # Обновление состояния трейта (качества)
            except AttributeError:
                pass

    # Метод получения индекса позиции объекта в сетке
    def getPosIndex(self):
        return Vec2D(self.rect.x // 32, self.rect.y // 32) # Возвращает экземпляр класса Vec2D с координатами X и Y, полученными делением координат прямоугольника на размер ячейки сетки

    # Метод получения индекса позиции объекта в виде чисел с плавающей запятой.
    def getPosIndexAsFloat(self):
        return Vec2D(self.rect.x / 32.0, self.rect.y / 32.0) # Возвращает экземпляр класса Vec2D с координатами X и Y, полученными делением координат прямоугольника на размер ячейки сетки в виде чисел с плавающей запятой.
