from enum import Enum


class GoodTypesEnum(str, Enum):
    NEW = "new"
    REGULAR = "regular"
    HIT = "hit"


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
