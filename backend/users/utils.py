def users_files_path(instance, filename) -> str:
    """Функция для формирования пути сохранения изображения.

    :param instance: Экземпляр модели.
    :param filename: Имя файла.
    :return: Путь к файлу.
    """
    filename = filename.split('.')
    instance_id = instance.id if instance.id else instance.user.id
    return f'users/{instance_id}/{instance.__class__.__name__}/{filename[0][:25]}.{filename[1]}'
