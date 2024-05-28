import pygame

from classes.Animation import Animation
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait


# В данном коде реализован класс Koopa, представляющий вражеского моба в игре, с методами для обновления его состояния,
# отрисовки на экране, обработки столкновений и других действий в зависимости от текущего состояния объекта.

class Koopa(EntityBase):
    def __init__(self, screen, spriteColl, x, y, level, sound):
        super(Koopa, self).__init__(y - 1, x, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("koopa-1").image,
                self.spriteCollection.get("koopa-2").image,
            ]
        )
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level)
        self.timer = 0
        self.timeAfterDeath = 35
        self.type = "Mob"
        self.dashboard = level.dashboard
        self.collision = Collider(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound

    # обновление состояние объекта Koopa в зависимости от его текущего состояния
    def update(self, camera):
        if self.alive and self.active:
            self.updateAlive(camera)
            self.checkEntityCollision()
        elif self.alive and not self.active and not self.bouncing:
            self.sleepingInShell(camera)
            self.checkEntityCollision()
        elif self.bouncing:
            self.shellBouncing(camera)

    # отрисовка Koopa на экране в соответствии с его направлением движения
    def drawKoopa(self, camera):
        if self.leftrightTrait.direction == -1:
            self.screen.blit(
                self.animation.image, (self.rect.x + camera.x, self.rect.y - 32)
            )
        else:
            self.screen.blit(
                pygame.transform.flip(self.animation.image, True, False),
                (self.rect.x + camera.x, self.rect.y - 32),
            )

    # отрисовка Koopa в панцире
    def shellBouncing(self, camera):
        self.leftrightTrait.speed = 4
        self.applyGravity()
        self.animation.image = self.spriteCollection.get("koopa-hiding").image
        self.drawKoopa(camera)
        self.leftrightTrait.update()

    # отрисовка Koopa в панцире
    def sleepingInShell(self, camera):
        if self.timer < self.timeAfterDeath:
            self.screen.blit(
                self.spriteCollection.get("koopa-hiding").image,
                (self.rect.x + camera.x, self.rect.y - 32),
            )
        else:
            self.alive = True
            self.active = True
            self.bouncing = False
            self.timer = 0
        self.timer += 0.1

    # обновление состояния объекта, когда он живой
    def updateAlive(self, camera):
        self.applyGravity()
        self.drawKoopa(camera)
        self.animation.update()
        self.leftrightTrait.update()

    # проверка на столкновения
    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            if ent is not self:
                collisionState = self.EntityCollider.check(ent)
                if collisionState.isColliding:
                    if ent.type == "Mob":
                        self._onCollisionWithMob(ent, collisionState)

    # обработка столкновения (звук)
    def _onCollisionWithMob(self, mob, collisionState):
        if collisionState.isColliding and mob.bouncing:
            self.alive = False
            self.sound.play_sfx(self.sound.brick_bump)
