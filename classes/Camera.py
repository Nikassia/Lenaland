from classes.Maths import Vec2D


class Camera:
    def __init__(self, pos, entity):
        self.pos = Vec2D(pos.x, pos.y) # Установка позиции камеры
        self.entity = entity # Установка сущности, за которой следит камера
        self.x = self.pos.x * 32 # Вычисление координаты x камеры в пикселях
        self.y = self.pos.y * 32

# Метод перемещения камеры
    def move(self):
        xPosFloat = self.entity.getPosIndexAsFloat().x # Получение плавающей координаты x сущности
        if 10 < xPosFloat < 50: # Проверка, находится ли сущность в определенном диапазоне по x
            self.pos.x = -xPosFloat + 10 # Перемещение камеры по x в зависимости от позиции сущности
        self.x = self.pos.x * 32 # Обновление координаты x камеры в пикселях
        self.y = self.pos.y * 32
