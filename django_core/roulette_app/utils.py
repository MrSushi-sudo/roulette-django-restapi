import random


def get_available_spins(array: list) -> list:
    """
    Функция для получения возможных спинов

    :param array: Предыдущие спины, по которым
    мы проверим, какие спины нужно исключить из
    итогового результата

    :return list: Все возможные спины
    """

    available_spins = [
        spin for spin in range(1, 11) \
        if spin not in array
    ]

    return available_spins


def get_spin(array: list) -> int:
    """
    Функция для получения спина

    :param array: Предыдущие спины, исходя
    из которых мы получим новый спин

    :return int: Новый спин
    """

    available_spins = get_available_spins(array)

    # если вернулся пустой массив, то это
    # заключающий раунд, мы должны вернуть
    # число 11
    if not available_spins:
        return 11

    # получаем рандомный спин
    spin = random.choice(available_spins)

    return spin
