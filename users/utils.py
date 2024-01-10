import random


def generate_password():
    """
    Функция для генерации числового пароля
    :return:
    """
    password = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return password
