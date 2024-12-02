"""
Модуль отвечает за еду.

Classes:
    Snake: Содержит методы возврата, получения положения сегментов змейки и ее головы,
    а также относящиеся к ее управлению.
"""

class Snake:
    """
    Содержит методы возврата, получения положения сегментов змейки и ее головы,
    а также относящиеся к ее управлению.
    """
    def __init__(
        self,
        *,
        segment_positions: list[tuple[int, int]],
        initial_direction: str
        ) -> None:
        """
        Инициализирует параметры для появления еды.

        Args:
            segment_positions (list[tuple[int, int]]): Позиции сегментов.
            initial_direction (str): Начальное направление.
        """
        self.__segment_positions = segment_positions
        self.__previous_positions = self.__segment_positions

        self.__direction = initial_direction

    def return_snake_to_previous_position(self, prev_position: list[tuple[int, int]]) -> None:
        """
        Возвращает змейку на предыдущее положение.

        Args:
            prev_position (list[tuple[int, int]]): Предыдущее положение змейки. 
        """
        self.__segment_positions = prev_position
    
    def get_previous_position(self) -> list[tuple[int, int]]:
        """
        Получает предыдущее положение змейки.

        Returns:
            list[tuple[int, int]]: Предыдущее положение змейки.
        """
        return self.__previous_positions

    def get_segment_positions(self) -> list[tuple[int, int]]:
        """
        Получает положение сегментов змейки.

        Returns:
            list[tuple[int, int]]: Положение сегментов змейки.
        """
        return self.__segment_positions

    def add_segment_to_end(self) -> None:
        """Добавляет сегмент в конец змейки."""
        tail = self.__segment_positions[-1]
        self.__segment_positions.append(tail)

    def get_head_position(self) -> tuple[int, int]:
        """
        Получает положение головы.

        Returns:
            tuple[int, int]: Положение головы.
        """
        return self.__segment_positions[0]

    def change_direction(self, new_direction: dict[str, str]) -> None:
        """
        Разрешает двигаться по новому направлению.

        Args:
            new_direction (dict[str, str]): Новое направление.
        """
        opposites = {
            'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'
            }
        if new_direction != opposites.get(self.__direction):
            self.__direction = new_direction

    def move(self) -> None:
        """Двигает змейку взависимости от направления."""
        self.__previous_positions = list(self.__segment_positions)

        head_x, head_y = self.__segment_positions[0]

        if self.__direction == 'Left':
            new_head = (head_x - 20, head_y)
        elif self.__direction == 'Right':
            new_head = (head_x + 20, head_y)
        elif self.__direction == 'Up':
            new_head = (head_x, head_y - 20)
        elif self.__direction == 'Down':
            new_head = (head_x, head_y + 20)

        self.__segment_positions = [new_head] + self.__segment_positions[:-1]
