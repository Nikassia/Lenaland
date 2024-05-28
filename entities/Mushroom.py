from classes.Animation import Animation
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider


# Этот код содержит методы для инициализации объекта (красного гриба), обновления его состояния, отображения на экране, обработки смерти и проверки столкновений с другими сущностями.

class RedMushroom(EntityBase):
    def __init__(self, screen, spriteColl, x, y, level, sound):
        super(RedMushroom, self).__init__(y, x - 1, 1.25) # Вызываем метод init из родительского класса EntityBase
        self.spriteCollection = spriteColl # Сохраняем коллекцию спрайтов в атрибуте spriteCollection
        self.animation = Animation(
            [
                self.spriteCollection.get("mushroom").image, # Создаем анимацию для гриба.
            ]
        )
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level) # Инициализируем лево-правую ходьбу для объекта
        self.type = "Mob" # Устанавливаем тип объекта
        self.dashboard = level.dashboard
        self.collision = Collider(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound

    def update(self, camera):
        if self.alive:
            self.applyGravity()
            self.drawRedMushroom(camera) # Рисуем объект на экране
            self.leftrightTrait.update() # Обновляем лево-правую ходьбу объекта
            self.checkEntityCollision() # Проверяем столкновения с другими сущностями
        else:
            self.onDead(camera)

    def drawRedMushroom(self, camera):
        self.screen.blit(self.animation.image, (self.rect.x + camera.x, self.rect.y)) # Отображаем объект на экране
        self.animation.update()

    def onDead(self, camera):
        if self.timer == 0:
            self.setPointsTextStartPosition(self.rect.x + 3, self.rect.y) # Устанавливаем позицию текста очков.
        if self.timer < self.timeAfterDeath:
            self.movePointsTextUpAndDraw(camera) # Двигаем текст с очками вверх и отображаем его.
        else:
            self.alive = None # Устанавливаем значение None для атрибута alive.
        self.timer += 0.1

    def setPointsTextStartPosition(self, x, y):
        self.textPos = Vec2D(x, y) # Устанавливаем позицию текста

    def movePointsTextUpAndDraw(self, camera):
        self.textPos.y += -0.5 # Двигаем текст вверх
        self.dashboard.drawText("100", self.textPos.x + camera.x, self.textPos.y, 8) # Отображаем текст с очками

    def checkEntityCollision(self):
        pass # Пропускаем проверку столкновения с другими сущностями.
