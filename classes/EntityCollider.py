# В представленном коде определены два класса: EntityCollider и CollisionState. Класс EntityCollider предоставляет методы для проверки столкновений между объектами, а класс CollisionState используется для хранения информации о результатах проверки столкновений.


class EntityCollider:
    def __init__(self, entity):
        self.entity = entity

    def check(self, target):
        if self.entity.rect.colliderect(target.rect): # Проверяем столкновение объекта с целью.
            return self.determineSide(target.rect, self.entity.rect) # Возвращаем результат проверки стороны столкновения.
        return CollisionState(False, False) # Если столкновения нет, возвращаем объект CollisionState с обоими значениями False

    def determineSide(self, rect1, rect2):
        if (
            rect1.collidepoint(rect2.bottomleft) # Проверяем, находится ли левый нижний угол rect2 внутри rect1.
            or rect1.collidepoint(rect2.bottomright) # Проверяем, находится ли правый нижний угол rect2 внутри rect1.
            or rect1.collidepoint(rect2.midbottom) # Проверяем, находится ли нижняя середина rect2 внутри rect1.
        ):
            if rect2.collidepoint(
                (rect1.midleft[0] / 2, rect1.midleft[1] / 2)
            ) or rect2.collidepoint((rect1.midright[0] / 2, rect1.midright[1] / 2)):
                return CollisionState(True, False) # Возвращаем объект CollisionState с isColliding=True и isTop=False.
            else:
                if self.entity.vel.y > 0: # Если скорость объекта по оси y больше 0 (движется вниз)
                    return CollisionState(True, True)
        return CollisionState(True, False) # Если не подошло ни одно из условий


class CollisionState:
    def __init__(self, _isColliding, _isTop):
        self.isColliding = _isColliding
        self.isTop = _isTop
