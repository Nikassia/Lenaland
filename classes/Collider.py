# Этот класс отвечает за обработку столкновений объектов с уровнем игры по осям X и Y, а также за проверку достижения границ уровня

class Collider:
    def __init__(self, entity, level):
        self.entity = entity
        self.level = level.level
        self.levelObj = level
        self.result = [] # Инициализируем пустой список result.

    # Метод для проверки столкновений по оси X.
    def checkX(self):
        if self.leftLevelBorderReached() or self.rightLevelBorderReached():
            return # Если достигнута левая или правая граница уровня, выходим из метода.
        try:
            rows = [
                self.level[self.entity.getPosIndex().y],
                self.level[self.entity.getPosIndex().y + 1],
                self.level[self.entity.getPosIndex().y + 2],
            ]
        except Exception:
            return # Если возникла ошибка, выходим из метода.
        for row in rows:
            tiles = row[self.entity.getPosIndex().x : self.entity.getPosIndex().x + 2]
            for tile in tiles:
                if tile.rect is not None:
                    if self.entity.rect.colliderect(tile.rect): # Проверяем столкновение объекта с тайлом и корректируем положение и скорость объекта при необходимости.
                        if self.entity.vel.x > 0:
                            self.entity.rect.right = tile.rect.left
                            self.entity.vel.x = 0
                        if self.entity.vel.x < 0:
                            self.entity.rect.left = tile.rect.right
                            self.entity.vel.x = 0

    # Метод для проверки столкновений по оси Y
    def checkY(self):
        self.entity.onGround = False
        
        try:
            rows = [
                self.level[self.entity.getPosIndex().y],
                self.level[self.entity.getPosIndex().y + 1],
                self.level[self.entity.getPosIndex().y + 2],
            ] # Получаем три строки для проверки столкновений.
        except Exception:
            try:
                self.entity.gameOver()
            except Exception:
                self.entity.alive = None
            return
        for row in rows:
            tiles = row[self.entity.getPosIndex().x : self.entity.getPosIndex().x + 2]
            for tile in tiles:
                if tile.rect is not None:
                    if self.entity.rect.colliderect(tile.rect): # Проверяем столкновение объекта с тайлом и корректируем положение и скорость объекта при необходимости.
                        if self.entity.vel.y > 0:
                            self.entity.onGround = True
                            self.entity.rect.bottom = tile.rect.top
                            self.entity.vel.y = 0
                            # reset jump on bottom
                            if self.entity.traits is not None:
                                if "JumpTrait" in self.entity.traits:
                                    self.entity.traits["JumpTrait"].reset()
                                if "bounceTrait" in self.entity.traits:
                                    self.entity.traits["bounceTrait"].reset()
                        if self.entity.vel.y < 0:
                            self.entity.rect.top = tile.rect.bottom
                            self.entity.vel.y = 0

    # Метод для проверки достижения правой границы уровня.
    def rightLevelBorderReached(self):
        if self.entity.getPosIndexAsFloat().x > self.levelObj.levelLength - 1: # Если объект достиг правой границы уровня, корректируем его положение и скорость
            self.entity.rect.x = (self.levelObj.levelLength - 1) * 32
            self.entity.vel.x = 0
            return True

    # Метод для проверки достижения левой границы уровня.
    def leftLevelBorderReached(self):
        if self.entity.rect.x < 0: # Если объект достиг левой границы уровня, корректируем его положение и скорость.
            self.entity.rect.x = 0
            self.entity.vel.x = 0
            return True
