"""
Модуль отвечает за экран игровых настроек.

Classes:
    SettingsScreen: Содержит функционал инициализации экрана игровых настроек 
    и создания его виджетов.

Imports:
    tkinter: Для написания аннотации типа аргумента master класса SettingsScreen.
    Callable: Для написания аннотации типа аргумента buttons класса SettingsScreen.

    Screen: Является родительским классом класса SettingsScreen.
"""
import tkinter as tk
from typing import Callable

from screens.screen import Screen


class SettingsScreen(Screen):
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

        self.__FONT = ('Arial', 20)
        self.__WIDGETS_WIDTH = 17
        self.__SCALES_LENGTH = 200
        self.__LABELS_PADY = 5
        self.__BUTTONS_PADY = 10
        
        self.__buttons = buttons

        self.__snake_colours = {
            'Зеленый': 'Green',
            'Синий': 'Blue',
            'Желтый': 'Yellow',
            'Фиолетовый': 'Purple',
            'Оранжевый': 'Orange'
            }

        self.__canvas_colours = {
            'Черный': 'Black',
            'Белый': 'White',
            'Серый': 'Gray',
            'Коричневый': 'Brown',
            'Розовый': 'Pink'
            }

    def get_settings(self) -> dict[str, int | str]:
        """
        Получает настройки игры.
        
        Returns: 
            dict[str, int | str]: Настройки игры.
        """
        snake_speed = self.snake_speed.get()
        snake_length = self.snake_length.get()
        snake_color = self.snake_color.get()
        canvas_color = self.canvas_color.get()
        settings = {
            'snake speed': snake_speed,
            'snake length': snake_length,
            'snake color': self.__snake_colours[snake_color],
            'canvas color': self.__canvas_colours[canvas_color]
            }
        return settings

    def __create_snake_speed_selection(self) -> None:
        """Создает выбор скорости змейки на экране."""
        speed_label = tk.Label(
            self.frame,
            text='Скорость змейки:',
            font=self.__FONT,
            width=self.__WIDGETS_WIDTH
            )
        speed_label.pack(pady=self.__LABELS_PADY)

        self.snake_speed = tk.IntVar(value=10)
        speed_scale = tk.Scale(
            self.frame,
            from_=5,
            to=15,
            font=self.__FONT,
            width=self.__WIDGETS_WIDTH,
            length=self.__SCALES_LENGTH,
            orient=tk.HORIZONTAL,
            variable=self.snake_speed
            )
        speed_scale.pack()

    def __create_snake_colour_selection(self) -> None:
        """Создает выбор цвета змейки на экране."""
        snake_color_label = tk.Label(
            self.frame,
            text='Цвет змейки:',
            font=self.__FONT,
            width=self.__WIDGETS_WIDTH
            )
        snake_color_label.pack(pady=self.__LABELS_PADY)

        self.snake_color = tk.StringVar(value='Зеленый')
        snake_color_options = [
            'Зеленый', 'Синий', 'Желтый', 'Фиолетовый', 'Оранжевый'
            ]
        snake_color_menu = tk.OptionMenu(
            self.frame, self.snake_color, *snake_color_options
            )
        snake_color_menu.config(
            font=self.__FONT, width=self.__WIDGETS_WIDTH
            )
        snake_color_menu.pack()
        menu = self.master.nametowidget(snake_color_menu.menuname)
        menu.config(font=self.__FONT)

    def __create_snake_lenght_selection(self) -> None:
        """Создает выбор длины змейки на экране."""
        length_label = tk.Label(
            self.frame,
            text='Длина змейки:',
            font=self.__FONT,
            width=self.__WIDGETS_WIDTH
            )
        length_label.pack(pady=self.__LABELS_PADY)

        self.snake_length = tk.IntVar(value=3)
        length_scale = tk.Scale(
            self.frame,
            from_=3,
            to=15,
            font=self.__FONT,
            width=self.__WIDGETS_WIDTH,
            length=self.__SCALES_LENGTH,
            orient=tk.HORIZONTAL,
            variable=self.snake_length
            )
        length_scale.pack()

    def __create_canvas_colour_selection(self) -> None:
        """Создает выбор цвета игрового холста на экране."""
        canvas_color_label = tk.Label(
            self.frame,
            text='Цвет игрового поля:',
            font=self.__FONT,
            width=self.__WIDGETS_WIDTH
            )
        canvas_color_label.pack(pady=self.__LABELS_PADY)

        self.canvas_color = tk.StringVar(value='Черный')
        canvas_color_options = [
            'Черный', 'Белый', 'Серый', 'Коричневый', 'Розовый'
            ]
        canvas_color_menu = tk.OptionMenu(
            self.frame, self.canvas_color, *canvas_color_options
            )
        canvas_color_menu.config(font=self.__FONT, width=self.__WIDGETS_WIDTH)
        canvas_color_menu.pack()
        menu = self.master.nametowidget(canvas_color_menu.menuname)
        menu.config(font=self.__FONT)

    def __create_buttons(self) -> None:
        """Создает кнопки на экране."""
        for key, value in self.__buttons.items():
            button = tk.Button(
                self.frame,
                text=key,
                font=self.__FONT,
                width=self.__WIDGETS_WIDTH,
                command=value
                )
            button.pack(pady=self.__BUTTONS_PADY)

    def create(self) -> None:
        """Создает виджеты экрана."""
        self.__create_snake_speed_selection()
        self.__create_snake_lenght_selection()
        self.__create_snake_colour_selection()
        self.__create_canvas_colour_selection()
        self.__create_buttons()
