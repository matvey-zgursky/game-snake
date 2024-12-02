"""
Модуль отвечает за экран справки.

Classes:
    HelpScreen: Содержит функционал инициализации экрана справки и создания 
    его виджетов.

Imports:
    tkinter: Для написания аннотации типа аргумента master класса HelpScreen.
    Callable: Для написания аннотации типа аргумента buttons класса HelpScreen.

    Screen: Является родительским классом класса HelpScreen.
"""
import tkinter as tk
from typing import Callable

from screens.screen import Screen


class HelpScreen(Screen):
    """
    Инициализирует экран с параметрами его виджетов, заданными кнопками и привязывает его 
    к родительскому окну.

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

        self.__FONT = ('Arial', 20)
        self.__WIDGETS_PADY = 20
        self.__HELP_TEXT = (
            'Управление змейкой осуществляется английской раскладкой:\n'
            ' - W: двигаться вверх\n'
            ' - A: двигаться влево\n'
            ' - S: двигаться вниз\n'
            ' - D: двигаться вправо\n'
            '\n'
            'Цель игры: собирать еду и избегать столкновения '
            'со стенами и со своим хвостом.'
            )
        
        self.__buttons = buttons

    def __create_help_text(self) -> None:
        """Создает текст справки на экране."""
        label = tk.Label(
            self.frame,
            text=self.__HELP_TEXT,
            font=self.__FONT,
            justify='left',
            wraplength=500
            )
        label.pack(pady=self.__WIDGETS_PADY)

    def __create_button(self) -> None:
        """Создает кнопку на экране."""
        for key, value in self.__buttons.items():
            button = tk.Button(
                master=self.frame,
                text=key,
                font=self.__FONT,
                width=15,
                command=value
                )
            button.pack(pady=self.__WIDGETS_PADY)

    def create(self) -> None:
        """Создает виджеты экрана."""
        self.__create_help_text()
        self.__create_button()
