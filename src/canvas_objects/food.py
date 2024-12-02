"""
Модуль отвечает за еду.

Classes:
    Food: Содержит методы задавания позиции новой еды и получения
    ее текущей позиции.

Imports:
    randint: Для определения случайной позиции еды.
"""
from random import randint


class Food:
    """
    Содержит методы задавания позиции новой еды и получения
    ее текущей позиции.
    """
    def __init__(
        self,
        *,
        canvas_width: int,
        canvas_heigth: int,
        cell_size: int
        ) -> None:
        """
        Инициализирует параметры для появления еды.

        Args:
            canvas_width (int): Ширина игрового холста.
            canvas_heigth(int): Высота игрового холста.
            cell_size(int): Размер еды.
        """
        self.__CANVAS_WIDTH = canvas_width
        self.__CANVAS_HEIGTH = canvas_heigth
        self.__CELL_SIZE = cell_size

        self.__position = ()

    def get_position(self) -> tuple[int, int]:
        """
        Получает позицию еды.

        Returns:
            tuple[int, int]: Позиция еды.
        """
        return self.__position
    
    def set_new_position(
        self, *, snake_positions: list[tuple[int, int]]
        ) -> None:
        """
        Задает новую позицию еды.

        Args:
            snake_positions (list[tuple[int, int]]): Позиции сегментов змейки.
        """
        while True:
            x = randint(0, (self.__CANVAS_WIDTH - self.__CELL_SIZE) \
                        // self.__CELL_SIZE) * self.__CELL_SIZE
            y = randint(0, (self.__CANVAS_HEIGTH - self.__CELL_SIZE) \
                        // self.__CELL_SIZE) * self.__CELL_SIZE
            position = (x, y)
            if position not in snake_positions:
                self.__position = position
                break
