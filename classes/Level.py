import json
import pygame

from classes.Sprites import Sprites
from classes.Tile import Tile
from entities.Coin import Coin
from entities.CoinBrick import CoinBrick
from entities.Goomba import Goomba
from entities.Mushroom import RedMushroom
from entities.Koopa import Koopa
from entities.CoinBox import CoinBox
from entities.RandomBox import RandomBox


# Этот код описывает класс `Level`, который представляет игровой уровень
# Он содержит методы для загрузки уровня из JSON файла, загрузки объектов и сущностей на уровне,
# обновления сущностей и отрисовки уровня на экране

class Level:
    def __init__(self, screen, sound, dashboard):
        self.sprites = Sprites() # Создание объекта Sprites
        self.dashboard = dashboard
        self.sound = sound
        self.screen = screen
        self.level = None
        self.levelLength = 0
        self.entityList = [] # Список сущностей на уровне

    # Метод загрузки уровня из JSON файла
    def loadLevel(self, levelname):
        with open("./levels/{}.json".format(levelname)) as jsonData:
            data = json.load(jsonData)
            self.loadLayers(data) # Загрузка слоев уровня
            self.loadObjects(data) # Загрузка объектов на уровне
            self.loadEntities(data) # Загрузка сущностей на уровне
            self.levelLength = data["length"]

    # Метод загрузки сущностей на уровне из JSON данных
    def loadEntities(self, data):
        try:
            [self.addCoinBox(x, y) for x, y in data["level"]["entities"]["CoinBox"]]
            [self.addGoomba(x, y) for x, y in data["level"]["entities"]["Goomba"]]
            [self.addKoopa(x, y) for x, y in data["level"]["entities"]["Koopa"]]
            [self.addCoin(x, y) for x, y in data["level"]["entities"]["coin"]]
            [self.addCoinBrick(x, y) for x, y in data["level"]["entities"]["coinBrick"]]
            [self.addRandomBox(x, y, item) for x, y, item in data["level"]["entities"]["RandomBox"]]
        except:
            # Обработка исключения, если нет сущностей на уровне
            pass

    # Метод загрузки слоев уровня из JSON данных
    def loadLayers(self, data):
        layers = []
        for x in range(*data["level"]["layers"]["sky"]["x"]):
            layers.append(
                (
                        [
                            Tile(self.sprites.spriteCollection.get("sky"), None)
                            for y in range(*data["level"]["layers"]["sky"]["y"])
                        ]
                        + [
                            Tile(
                                self.sprites.spriteCollection.get("ground"),
                                pygame.Rect(x * 32, (y - 1) * 32, 32, 32),
                            )
                            for y in range(*data["level"]["layers"]["ground"]["y"])
                        ]
                )
            )
        self.level = list(map(list, zip(*layers))) # Формирование уровня из слоев

    # Метод загрузки объектов на уровне из JSON данных
    def loadObjects(self, data):
        for x, y in data["level"]["objects"]["bush"]:
            self.addBushSprite(x, y)
        for x, y in data["level"]["objects"]["cloud"]:
            self.addCloudSprite(x, y)
        for x, y, z in data["level"]["objects"]["pipe"]:
            self.addPipeSprite(x, y, z)
        for x, y in data["level"]["objects"]["sky"]:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("sky"), None)
        for x, y in data["level"]["objects"]["ground"]:
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("ground"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )

    # Метод обновления сущностей на уровне
    def updateEntities(self, cam):
        for entity in self.entityList:
            entity.update(cam)
            if entity.alive is None:
                self.entityList.remove(entity)

    # Метод отрисовки уровня на экране с учетом камеры
    def drawLevel(self, camera):
        try:
            for y in range(0, 15):
                for x in range(0 - int(camera.pos.x + 1), 20 - int(camera.pos.x - 1)):
                    if self.level[y][x].sprite is not None:
                        if self.level[y][x].sprite.redrawBackground:
                            self.screen.blit(
                                self.sprites.spriteCollection.get("sky").image,
                                ((x + camera.pos.x) * 32, y * 32),
                            )
                        self.level[y][x].sprite.drawSprite(
                            x + camera.pos.x, y, self.screen
                        )
            self.updateEntities(camera) # Обновление сущностей на уровне с учетом камеры
        except IndexError:
            return

    # Добавляет спрайт облака на уровень
    def addCloudSprite(self, x, y):
        try:
            for yOff in range(0, 2):
                for xOff in range(0, 3):
                    self.level[y + yOff][x + xOff] = Tile(
                        self.sprites.spriteCollection.get("cloud{}_{}".format(yOff + 1, xOff + 1)), None, )
        except IndexError:
            return

    # Добавляет спрайт трубы на уровень, включая верх и тело трубы заданной длины
    def addPipeSprite(self, x, y, length=2):
        try:
            # добавление верха трубы
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("pipeL"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("pipeR"),
                pygame.Rect((x + 1) * 32, y * 32, 32, 32),
            )
            # добавление тела трубы
            for i in range(1, length + 20):
                self.level[y + i][x] = Tile(
                    self.sprites.spriteCollection.get("pipe2L"),
                    pygame.Rect(x * 32, (y + i) * 32, 32, 32),
                )
                self.level[y + i][x + 1] = Tile(
                    self.sprites.spriteCollection.get("pipe2R"),
                    pygame.Rect((x + 1) * 32, (y + i) * 32, 32, 32),
                )
        except IndexError:
            return

    # Добавляет спрайты кустов на уровень.
    def addBushSprite(self, x, y):
        try:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("bush_1"), None)
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("bush_2"), None
            )
            self.level[y][x + 2] = Tile(
                self.sprites.spriteCollection.get("bush_3"), None
            )
        except IndexError:
            return

    # Добавляет спрайт коробки с монетами на уровень и создает объект CoinBox
    def addCoinBox(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            CoinBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.sound,
                self.dashboard,
            )
        )

    # Добавляет спрайт случайной коробки на уровень и создает объект RandomBox с заданным предметом
    def addRandomBox(self, x, y, item):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            RandomBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                item,
                self.sound,
                self.dashboard,
                self
            )
        )

    # Добавляет монету на уровень
    def addCoin(self, x, y):
        self.entityList.append(Coin(self.screen, self.sprites.spriteCollection, x, y))

    # Добавляет спрайт коробки с монетой на уровень и создает объект CoinBrick.
    def addCoinBrick(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            CoinBrick(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.sound,
                self.dashboard
            )
        )

    # Добавляет объект  Goomba (враждебного персонажа) на уровень
    def addGoomba(self, x, y):
        self.entityList.append(
            Goomba(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )

    # Добавляет объект Koopa (враждебный персонаж) на уровень
    def addKoopa(self, x, y):
        self.entityList.append(
            Koopa(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )

    # Добавляет объект RedMushroom (гриб) на уровень
    def addRedMushroom(self, x, y):
        self.entityList.append(
            RedMushroom(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )
