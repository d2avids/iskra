def users_photo_path(instance, filename) -> str:
    """Функция для формирования пути сохранения изображения.

    :param instance: Экземпляр модели.
    :param filename: Имя файла. Добавляем к имени текущую дату и время.
    :return: Путь к изображению.
    Сохраняем в users/{user_id}/photo
    """
    return f'users/{instance.id}/photo'
