"""
Модуль отвечает за стартовый экран.

Classes:
    StartScreen: Содержит функционал инициализации экрана стартового экрана
    и создания его виджетов.

Imports:
    tkinter: Для написания аннотации типа аргумента master класса StartScreen.
    Callable: Для написания аннотации типа аргумента buttons класса StartScreen.

    Screen: Является родительским классом класса StartScreen.
"""
import tkinter as tk
from collections.abc import Callable
from screens.screen import Screen


class StartScreen(Screen):
    """
    Содержит функционал инициализации и создания виджетов экрана.

    Attributes:
        master (Tk): Родительское окно.
        frame (Frame): Сам экран.
    """
    def __init__(
        self, *, master: tk.Tk, buttons: dict[str, Callable[[], None]]
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

        self.__MAIN_FONT = ('Arial', 25)
        self.__WIDGETS_WIDTH = 15
        self.__MAIN_PADY = 20

        self.__buttons = buttons

    def __create_game_name(self) -> None:
        """Создает название игры на экране."""
        name_label = tk.Label(
            self.frame,
            text='ЗМЕЙКА',
            font=('Cascadia Code', self.__MAIN_FONT[1] * 2),
            fg='green',
            width=self.__WIDGETS_WIDTH
            )
        name_label.pack(pady=self.__MAIN_PADY * 2)

    def __create_buttons(self) -> None:
        """Создает кнопки на экране."""
        for key, value in self.__buttons.items():
            button = tk.Button(
                master=self.frame,
                text=key,
                font=self.__MAIN_FONT,
                width=self.__WIDGETS_WIDTH,
                command=value
                )
            button.pack(pady=self.__MAIN_PADY)

    def create(self) -> None:
        """Создает виджеты экрана."""
        self.__create_game_name()
        self.__create_buttons()
