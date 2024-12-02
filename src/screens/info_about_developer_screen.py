"""
Модуль отвечает за экран "О разработчике".

Classes:
    AboutDeveloperScreen: Содержит функционал инициализации экрана "О разработчике" 
    и создания его виджетов.

Imports:
    tkinter: Для написания аннотации типа аргумента master класса AboutDeveloperScreen.
    Callable: Для написания аннотации типа аргумента buttons класса AboutDeveloperScreen.

    Screen: Является родительским классом класса AboutDeveloperScreen.
"""
import tkinter as tk
from typing import Callable

from screens.screen import Screen

class AboutDeveloperScreen(Screen):
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

        self.__FONT = ('Arial', 20)
        self.__WIDGETS_PADY = 20
        self.__DEVELOPER_TEXT = (
            'Создатель проекта студент 2 курса.\n'
            '\n'
            'Предлагайте работу за МНОГО-МНОГО денег!!!'
        )

        self.__buttons = buttons

    def __create_info_about_developer(self) -> None:
        """Создает текст информации о разработчике на экране."""
        label = tk.Label(
            self.frame,
            text=self.__DEVELOPER_TEXT,
            font=self.__FONT,
            wraplength=550
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
        self.__create_info_about_developer()
        self.__create_button()
