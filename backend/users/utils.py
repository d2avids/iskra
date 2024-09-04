def users_files_path(instance, filename) -> str:
    """Функция для формирования пути сохранения изображения.

    :param instance: Экземпляр модели.
    :param filename: Имя файла.
    :return: Путь к файлу.
    """
    filename = filename.split('.')
    return f'users/{instance.__class__.__name__}/{filename[0][:25]}.{filename[1]}'
