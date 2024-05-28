import json

from classes.Animation import Animation
from classes.Sprite import Sprite
from classes.Spritesheet import Spritesheet

# Этот код представляет собой класс Sprites,
# который загружает спрайты из JSON-файлов и создает объекты Sprite на основе этих данных

class Sprites:
    # Инициализация класса, загрузка спрайтов из указанных JSON-файлов
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./sprites/Mario.json",
                "./sprites/Goomba.json",
                "./sprites/Koopa.json",
                "./sprites/Animations.json",
                "./sprites/BackgroundSprites.json",
                "./sprites/ItemAnimations.json",
                "./sprites/RedMushroom.json"
            ]
        )

    # Загрузка спрайтов из списка URL-адресов файлов
    def loadSprites(self, urlList):
        resDict = {} # Создание пустого словаря для хранения загруженных спрайтов.
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData) # Открытие JSON-файла и загрузка данных
                mySpritesheet = Spritesheet(data["spriteSheetURL"]) # Создание объекта Spritesheet на основе URL-адреса файла с изображениями
                dic = {}
                # Проверка типа спрайта (background, animation, character или item) и создание объектов Sprite в соответствии с этим типом
                if data["type"] == "background":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                            ),
                            sprite["collision"],
                            None,
                            sprite["redrawBg"],
                        )
                    resDict.update(dic) # Добавление созданных спрайтов в словарь resDict
                    continue
                elif data["type"] == "animation":
                    for sprite in data["sprites"]:
                        images = []
                        for image in sprite["images"]:
                            images.append(
                                mySpritesheet.image_at(
                                    image["x"],
                                    image["y"],
                                    image["scale"],
                                    colorkey=sprite["colorKey"],
                                )
                            )
                        dic[sprite["name"]] = Sprite(
                            None,
                            None,
                            animation=Animation(images, deltaTime=sprite["deltaTime"]),
                        )
                    resDict.update(dic)
                    continue
                elif data["type"] == "character" or data["type"] == "item":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        try:
                            xSize = sprite['xsize']
                            ySize = sprite['ysize']
                        except KeyError:
                            xSize, ySize = data['size']
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                                True,
                                xTileSize=xSize,
                                yTileSize=ySize,
                            ),
                            sprite["collision"],
                        )
                    resDict.update(dic)
                    continue
        return resDict # Возврат словаря resDict, содержащего загруженные спрайты
