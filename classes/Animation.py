class Animation:
    def __init__(self, images, idleSprite=None, airSprite=None, deltaTime=7): # Инициализация класса с параметрами images (список изображений), idleSprite (спрайт покоя), airSprite (спрайт в воздухе), deltaTime (интервал времени между сменой изображений)
        self.images = images
        self.timer = 0
        self.index = 0
        self.image = self.images[self.index] # Присвоение атрибуту image первого изображения из списка images
        self.idleSprite = idleSprite
        self.airSprite = airSprite
        self.deltaTime = deltaTime

    # Метод обновления анимации
    def update(self):
        self.timer += 1
        if self.timer % self.deltaTime == 0: # Если прошло достаточно времени согласно deltaTime
            if self.index < len(self.images) - 1: # Если индекс меньше чем количество изображений минус 1
                self.index += 1 # Увеличение индекса на 1 для переключения на следующее изображение
            else:
                self.index = 0  # Если достигнут конец списка изображений, вернуться к началу.
        self.image = self.images[self.index]

    # Метод установки спрайта покоя
    def idle(self):
        self.image = self.idleSprite

    # Метод установки спрайта в воздухе
    def inAir(self):
        self.image = self.airSprite
