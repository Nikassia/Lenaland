class Sprite:
    def __init__(self, image, colliding, animation=None, redrawBackground=False):
        self.image = image
        self.colliding = colliding
        self.animation = animation
        self.redrawBackground = redrawBackground

    # Метод отрисовки спрайта на экране
    def drawSprite(self, x, y, screen):
        dimensions = (x * 32, y * 32) # Вычисление координат для отрисовки спрайта
        if self.animation is None: # Если у спрайта нет анимации
            screen.blit(self.image, dimensions) # Отрисовать изображение спрайта на экране
        else:
            self.animation.update() # Обновить анимацию спрайта
            screen.blit(self.animation.image, dimensions) # Отрисовать текущее изображение анимации спрайта на экране по заданным координатам
