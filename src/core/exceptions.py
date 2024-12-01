from fastapi import HTTPException, status


good_group_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Группа номенклатуры не найдена.",
)

specification_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Характеристика номенклатуры не найдена.",
)

good_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Товар не найден.",
)

good_in_good_not_found_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Нельзя удалить товар, которого нет в корзине.",
)

property_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Свойство не найдено.",
)

price_type_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Вид цены номенклатуры не найден.",
)

upload_image_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка при загрузке изображения в S3.",
)

encoded_image_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка при преобразовании base64 строки в изображение.",
)

incorrect_in_stock_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="`in_stock` не может быть меньше 0.",
)

incorrect_contact_me_form_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Должно быть заполнено хотя бы одно из полей: `phone` или `email`.",
)

contact_me_form_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Не удалось отправить форму обратной связи в 1С.",
)

invalid_creds_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный логин или пароль.",
)

outlets_json_decode_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка декодирования полученного списка торговых точек из 1С.",
)

outlets_validate_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка валидации полученного списка торговых точек из 1С.",
)

outlets_1c_error_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка получения списка торговых точек из 1С.",
)

cart_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Корзина для данной торговой точки не найдена.",
)

no_good_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Нельзя добавить товар, которого недостаточно на складе.",
)

no_good_with_the_price_type_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Нельзя добавить товар с данным `price_type_guid`.",
)

no_auth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Для работы с данным ресурсом требуется авторизация.",
)

access_denied_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Нет доступа к ресурсу.",
)

expired_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек.",
)

no_goods_specs_associations_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="У данного товара отсутствует указанная характеристика.",
)

invalid_quantity_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Количество товара не может быть меньше 1.",
)

no_cart_goods_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Товар отсутствует в корзине.",
)

no_price_type_guid_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Нельзя отфильтровать товары по цене без указания `price_type_guid`.",
)

favorites_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Избранное для данной торговой точки не найдено.",
)
