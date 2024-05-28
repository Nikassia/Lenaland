from classes.Animation import Animation
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait


class Goomba(EntityBase):
    def __init__(self, screen, spriteColl, x, y, level, sound):
        super(Goomba, self).__init__(y, x - 1, 1.25) # Вызов конструктора родительского класса EntityBase с передачей параметров
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("goomba-1").image,
                self.spriteCollection.get("goomba-2").image,
            ]
        ) # Создание объекта Animation с передачей списка изображений спрайтов goomba-1 и goomba-2
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level)
        self.type = "Mob"
        self.dashboard = level.dashboard
        self.collision = Collider(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound
        self.textPos = Vec2D(0, 0) # Создание объекта Vec2D для хранения позиции текста

    def update(self, camera):
        if self.alive:
            self.applyGravity()
            self.drawGoomba(camera) # Отобразить Гумбу на экране
            self.leftrightTrait.update() # Обновить состояние Гумбы (ходьба влево/вправо)
            self.checkEntityCollision() # Проверить столкновение с другими объектами
        else:
            self.onDead(camera)

    def drawGoomba(self, camera):
        self.screen.blit(self.animation.image, (self.rect.x + camera.x, self.rect.y)) # Отобразить изображение анимации Гумбы на экране
        self.animation.update() # Обновить анимацию Гумбы

    def onDead(self, camera):
        if self.timer == 0: # Если таймер равен 0
            self.setPointsTextStartPosition(self.rect.x + 3, self.rect.y) # Установить начальную позицию текста очков
        if self.timer < self.timeAfterDeath: # Если таймер меньше времени после смерти
            self.movePointsTextUpAndDraw(camera) # Переместить текст очков вверх и отобразить его на экране
            self.drawFlatGoomba(camera) # Отобразить сплющенного Гумбу на экране
        else:
            self.alive = None
        self.timer += 0.1

    def drawFlatGoomba(self, camera):
        self.screen.blit(
            self.spriteCollection.get("goomba-flat").image, # Отобразить сплющенного Гумбу на экране
            (self.rect.x + camera.x, self.rect.y),
        )

    def setPointsTextStartPosition(self, x, y):
        self.textPos = Vec2D(x, y) # Установить начальную позицию текста очков

    def movePointsTextUpAndDraw(self, camera):
        self.textPos.y += -0.5 # Переместить текст очков вверх по оси y
        self.dashboard.drawText("100", self.textPos.x + camera.x, self.textPos.y, 8) # Отобразить текст "100" на экране

    def checkEntityCollision(self):
        for ent in self.levelObj.entityList: # Для каждого объекта в списке entityList уровня
            collisionState = self.EntityCollider.check(ent) # Проверить столкновение с объектом ent
            if collisionState.isColliding:
                if ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState) # Выполнить действия при столкновении с типом Mob

    def _onCollisionWithMob(self, mob, collisionState):
        if collisionState.isColliding and mob.bouncing: # Если произошло столкновение и объект Mob отскакивает
            self.alive = False # Установить значение False для атрибута alive
            self.sound.play_sfx(self.sound.brick_bump) # Воспроизвести звук столкновения
