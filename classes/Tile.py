import pygame


# Этот код определяет класс Tile, который представляет собой плитку в игровом мире.
# Метод drawRect используется для отрисовки прямоугольника на экране с помощью библиотеки Pygame

class Tile:
    def __init__(self, sprite, rect):
        self.sprite = sprite # Присвоение атрибуту sprite переданного значения
        self.rect = rect

    def drawRect(self, screen): # Присвоение атрибуту sprite переданного значения
        try:
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), self.rect, 1) # Отрисовка прямоугольника на экране screen. Цвет - красный (255, 0, 0), толщина линии - 1
        except Exception:
            pass
