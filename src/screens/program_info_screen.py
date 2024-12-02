"""
Модуль отвечает за экран "О программе".

Classes:
    ProgramInfoScreen: Содержит функционал инициализации экрана "О программе" 
    и создания его виджетов.

Imports:
    tkinter: Для написания аннотации типа аргумента master класса ProgramInfoScreen.
    Callable: Для написания аннотации типа аргумента buttons класса ProgramInfoScreen.

    Screen: Является родительским классом класса ProgramInfoScreen.
"""
import tkinter as tk
from typing import Callable

from screens.screen import Screen


class ProgramInfoScreen(Screen):
    """
    Содержит функционал инициализации и создания виджетов экрана.

    Attributes:
        master (Tk): Родительское окно.
        frame (Frame): Сам экран.
    """
    def __init__(self, *, master: tk.Tk, buttons: dict[str, Callable[[], None]]) -> None:
        """
        Инициализирует экран и привязывает его к родительскому окну.

        Args:
            master (Tk): Родительское окно.
            buttons (dict[str, Callable[[], None]]): Словарь кнопок с \
                их названиями и функциями обратного вызова.
        """
        self.master = master
        self.frame = tk.Frame(self.master)

        self.__buttons = buttons

    def __create_buttons(self) -> None:
        """Создает кнопки на экране."""
        for key, value in self.__buttons.items():
            button = tk.Button(
                master=self.frame,
                text=key,
                font=('Arial', 24),
                width=20,
                command=value
            )
            button.pack(pady=20)

    def create(self) -> None:
        """Создает виджеты экрана."""
        self.__create_buttons()
