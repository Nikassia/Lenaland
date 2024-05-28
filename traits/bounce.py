# Реализация функционала прыжка

class bounceTrait:
    def __init__(self, entity):
        self.vel = 5 # Начальное значение скорости прыжка
        self.jump = False
        self.entity = entity

    def update(self):
        if self.jump:
            self.entity.vel.y = 0
            self.entity.vel.y -= self.vel # Вычитаем значение vel из вертикальной скорости объекта entity, чтобы сделать прыжок вверх
            self.jump = False # Предотвращаем повторный прыжок
            self.entity.inAir = True

    def reset(self):
        self.entity.inAir = False
