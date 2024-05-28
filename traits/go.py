from pygame.transform import flip


# Методы для управления движением объекта, обновления анимаций и отображения на экране в нужном направлении

class GoTrait:
    def __init__(self, animation, screen, camera, ent):
        self.animation = animation
        self.direction = 0
        self.heading = 1 # Направление взгляда
        self.accelVel = 0.4 # Скорость ускорения
        self.decelVel = 0.25 # Скорость замедления
        self.maxVel = 3.0 # Максимальная скорость
        self.screen = screen
        self.boost = False
        self.camera = camera
        self.entity = ent

# Обновление состояния объекта
    def update(self):
        if self.boost:
            self.maxVel = 5.0
            self.animation.deltaTime = 4
        else:
            self.animation.deltaTime = 7
            if abs(self.entity.vel.x) > 3.2:
                self.entity.vel.x = 3.2 * self.heading
            self.maxVel = 3.2

        if self.direction != 0:
            self.heading = self.direction
            if self.heading == 1:
                if self.entity.vel.x < self.maxVel:
                    self.entity.vel.x += self.accelVel * self.heading
            else:
                if self.entity.vel.x > -self.maxVel:
                    self.entity.vel.x += self.accelVel * self.heading

            if not self.entity.inAir:
                self.animation.update()
            else:
                self.animation.inAir()
        else:
            self.animation.update()
            if self.entity.vel.x >= 0:
                self.entity.vel.x -= self.decelVel
            else:
                self.entity.vel.x += self.decelVel
            if int(self.entity.vel.x) == 0:
                self.entity.vel.x = 0
                if self.entity.inAir:
                    self.animation.inAir()
                else:
                    self.animation.idle()
        if (self.entity.invincibilityFrames//2) % 2 == 0:
            self.drawEntity() # Отображение на экране с учетом направления

# Обновление анимации на основе новых данных
    def updateAnimation(self, animation):
        self.animation = animation
        self.update()

# Отрисовка на экране с учетом направления движения
    def drawEntity(self):
        if self.heading == 1:
            self.screen.blit(self.animation.image, self.entity.getPos())
        elif self.heading == -1:
            self.screen.blit(
                flip(self.animation.image, True, False), self.entity.getPos()
            )
