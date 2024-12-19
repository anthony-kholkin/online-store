from enum import Enum


class GoodTypesEnum(str, Enum):
    NEW = "new"
    HIT = "hit"
    REGULAR = "regular"


class PropertyNamesEnum(str, Enum):
    FILLING = "Начинка"
    FLAVOR = "Аромат"
    STRENGTH = "Крепость"
    FORMAT = "Формат"
    MANUFACTURING_METHOD = "Метод изготовления"
    PACKAGING = "Упаковка"
    BLOCK = "Блок"
    BOX = "Короб"


class OrderStatusEnum(str, Enum):
    OPEN = "Открыт"
    IN_PROCESS = "Обрабатывается"
    DONE = "Исполнен"


class OrderByEnum(str, Enum):
    NAME = "name"
    PRICE = "price"
    TYPE = "type"
