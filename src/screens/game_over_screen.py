"""
Модуль отвечает за экран проигрыша.

Classes:
    GameOverScreen: Содержит функционал инициализации экрана проигрыша и создания 
    его виджетов.

Imports:
    tkinter: Для написания аннотации типа аргумента master класса GameOverScreen.
    Callable: Для написания аннотации типа аргумента buttons класса GameOverScreen.

    Screen: Является родительским классом класса GameOverScreen.
"""
import tkinter as tk
from collections.abc import Callable

from screens.screen import Screen


class GameOverScreen(Screen):
    """
    Содержит функционал инициализации и создания виджетов экрана.

    Attributes:
        master (Tk): Родительское окно.
        frame (Frame): Сам экран.
    """
    def __init__(
        self,
        *,
        master: tk.Tk,
        buttons: dict[str, Callable[[], None]],
        score: int,
        record: int
        ) -> None:
        """
        Инициализирует экран и привязывает его к родительскому окну.

        Args:
            master (Tk): Родительское окно.
            buttons (dict[str, Callable[[], None]]): Словарь кнопок с \
                их названиями и функциями обратного вызова.
        """
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True)

        self.__MAIN_FONT = ('Arial', 20)
        self.__MAIN_PADY = 10

        self.__buttons = buttons
        self.__score = score
        self.__record = record

    def __create_game_over(self) -> None:
        """Создает надпись о проигрыше на экране."""
        label = tk.Label(
            self.frame,
            text='Вы проиграли!',
            font=(self.__MAIN_FONT[0], self.__MAIN_FONT[1] * 2)
            )
        label.pack(pady=self.__MAIN_PADY)

    def __create_score(self) -> None:
        """Создает заработанные очки на экране."""
        score_label = tk.Label(
            self.frame, text=f'Счет: {self.__score}', font=self.__MAIN_FONT
            )
        score_label.pack(pady=self.__MAIN_PADY / 2)

    def __create_record(self) -> None:
        """Создает рекорд очков на экране."""
        record_label = tk.Label(
            self.frame, text=f'Рекорд: {self.__record}', font=self.__MAIN_FONT
            )
        record_label.pack(pady=self.__MAIN_PADY)

    def __create_buttons(self) -> None:
        """Создает кнопки на экране."""
        for key, value in self.__buttons.items():
            button = tk.Button(
                master=self.frame,
                text=key,
                font=self.__MAIN_FONT,
                width=15,
                command=value
                )
            button.pack(pady=self.__MAIN_PADY)

    def create(self) -> None:
        """Создает виджеты экрана."""
        self.__create_game_over()
        self.__create_score()
        self.__create_record()
        self.__create_buttons()
