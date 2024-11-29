from enum import Enum


class GoodTypesEnum(Enum):
    NEW = "new"
    REGULAR = "regular"
    HIT = "hit"


class PropertyNamesEnum(Enum):
    FILLING = "Начинка"
    FLAVOR = "Аромат"
    STRENGTH = "Крепость"
    FORMAT = "Формат"
    MANUFACTURING_METHOD = "Метод изготовления"
    PACKAGING = "Упаковка"
    BLOCK = "Блок"
    BOX = "Короб"
