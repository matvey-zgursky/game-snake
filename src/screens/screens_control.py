"""
Модуль отвечает за инициализацию, создание экранов и их переключение.

Classes:
    ScreensControl: Содержит инициализацию, создание экранов и переключение между ними.

Imports:
    tkinter: Для написания аннотации типа аргумента master класса ScreensControl.
    Callable: Для написания аннотации типа аргумента quit_callback класса ScreensControl.
    
    StartScreen: Для инициализации, создания стартового экрана и его переключения. 
    SettingsScreen: Для инициализации, создания экрана настроек и его переключения. 
    HelpScreen: Для инициализации, создания экрана справки и его переключения. 
    AboutDeveloperScreen: Для инициализации, создания экрана "О разработчике" и его переключения. 
    GameScreen: Для инициализации, создания игрового экрана и его переключения. 
    GameOverScreen: Для инициализации, создания экрана проигрыша и его переключения. 
"""
import tkinter as tk
from typing import Callable

from screens.start_screen import StartScreen
from screens.settings_screen import SettingsScreen
from screens.program_info_screen import ProgramInfoScreen
from screens.help_screen import HelpScreen
from screens.info_about_developer_screen import AboutDeveloperScreen
from screens.game_screen import GameScreen
from screens.game_over_screen import GameOverScreen


class ScreensControl:
    """
    Отвечает за создание игровых экранов и переключение между ними.
    """
    def __init__(
        self, *, master: tk.Tk, quit_callback: Callable[[], None]
        ) -> None:
        """
        Инициализирует экземпляр ScreensControl.

        Args:
            master (Tk): Главное окно Tkinter.
            quit_callback (Callable[[], None]): Функция обратного вызова для выхода из приложения.
        """
        self.__master = master

        self.__record_score = 0

        self.__quit_callback = quit_callback

        self.__game_over_screen = None
        self.__game_screen = None

    def _show_info_about_program_screen(self) -> None:
        """Показывает экран информации о программе."""
        self.__start_screen.hide()
        self.__program_info_screen.show()

    def _show_settings_screen(self) -> None:
        """Показывает экран настроек."""
        self.__start_screen.hide()
        self.__settings_screen.show()

    def __create_start_screen(self) -> StartScreen:
        """
        Создает стартовый экран.

        Returns:
            StartScreen: Экземпляр стартового экрана.
        """
        start_screen = StartScreen(
            master=self.__master,
            buttons={
                'Играть': self._show_settings_screen,
                'О программе': self._show_info_about_program_screen,
                'Выход': self.__quit_callback
                }
            )
        start_screen.create()

        return start_screen

    def _show_help_screen(self) -> None:
        """Показывает экран справки."""
        self.__program_info_screen.hide()
        self.__help_screen.show()

    def _show_info_about_developer_screen(self) -> None:
        """Показывает экран информации о разработчике."""
        self.__program_info_screen.hide()
        self.__about_developer_screen.show()

    def _show_start_screen(self) -> None:
        """Показывает стартовый экран."""
        if self.__game_screen is not None:
            self.__game_screen.hide()

        if self.__game_over_screen is not None:
            self.__game_over_screen.hide()

        self.__program_info_screen.hide()
        self.__about_developer_screen.hide()
        self.__settings_screen.hide()
        self.__start_screen.show()

    def __create_program_info_screen(self) -> ProgramInfoScreen:
        """
        Создает экран информации о программе.

        Returns:
            ProgramInfoScreen: Экземпляр экрана информации о программе.
        """
        program_info_screen = ProgramInfoScreen(
            master=self.__master,
            buttons={
                'Справка': self._show_help_screen,
                'О разработке': self._show_info_about_developer_screen,
                'Назад': self._show_start_screen
                }
            )
        program_info_screen.create()
        
        return program_info_screen

    def _show_program_info_screen(self) -> None:
        """Показывает экран информации о программе."""
        self.__help_screen.hide()
        self.__about_developer_screen.hide()
        self.__program_info_screen.show()

    def __create_help_screen(self) -> HelpScreen:
        """
        Создает экран справки.

        Returns:
            HelpScreen: Экземпляр экрана справки.
        """
        help_screen = HelpScreen(
            master=self.__master,
            buttons={'Назад': self._show_program_info_screen}
            )
        help_screen.create()

        return help_screen

    def __create_info_about_developer_screen(self) -> AboutDeveloperScreen:
        """
        Создает экран информации о разработчике.

        Returns:
            AboutDeveloperScreen: Экземпляр экрана информации о разработчике.
        """
        about_developer_screen = AboutDeveloperScreen(
            master=self.__master,
            buttons={'Назад': self._show_program_info_screen}
            )
        about_developer_screen.create()

        return about_developer_screen

    def _restart_game_screen(self) -> None:
        """Перезапускает игровой экран."""
        self.__game_over_screen.hide()
        self.__game_screen.show()

    def _show_game_over_screen(self, score: int, record_score: int) -> None:
        """
        Показывает экран окончания игры.

        Args:
            score (int): Заработанные очки.
            record_score (int): Рекорд очков игрока.
        """
        if record_score > self.__record_score:
            self.__record_score = record_score

        self.__game_over_screen = self.__create_game_over_screen(score)
        self.__game_over_screen.show()

    def __create_game_over_screen(self, score: int) -> GameOverScreen:
        """
        Создает экран окончания игры.

        Args:
            score (int): Игровые очки

        Returns:
            GameOverScreen: Экземпляр экрана окончания игры.
        """
        game_over_screen = GameOverScreen(
            master=self.__master,
            buttons={
                'Рестарт': self._restart_game_screen,
                'Главное меню': self._show_start_screen,
                'Выход': self.__quit_callback
                },
            score=score,
            record=self.__record_score
            )
        game_over_screen.create()

        return game_over_screen

    def get_game_settings(self) -> dict[str, int | str]:
        """
        Получает текущие настройки игры.

        Returns:
            dict[str, int | str]: Настройки игры.
        """
        game_settings = self.__settings_screen.get_settings()
        
        return game_settings

    def __create_game_screen(self) -> GameScreen:
        """
        Создает экран игры с учетом настроек.

        Returns:
            GameScreen: Экземпляр экрана игры.
        """
        game_settings = self.get_game_settings()
        game_screen = GameScreen(
            master=self.__master,
            buttons={'Главное меню': self._show_start_screen},
            game_over_callback=self._show_game_over_screen,
            record_score=self.__record_score,
            settings=game_settings
            )
        game_screen.create()

        return game_screen

    def _show_game_screen(self) -> None:
        """Показывает экран игры."""
        self.__settings_screen.hide()
        self.__game_screen = self.__create_game_screen()
        self.__game_screen.show()

    def __create_settings_screen(self) -> SettingsScreen:
        """
        Создает экран настроек.

        Returns:
            SettingsScreen: Экземпляр экрана настроек.
        """
        settings_screen = SettingsScreen(
            master=self.__master,
            buttons={
                'Продолжить': self._show_game_screen,
                'Назад': self._show_start_screen
                }
            )
        settings_screen.create()
        return settings_screen

    def create_screens(self) -> None:
        """Создает игровые экраны."""
        self.__start_screen = self.__create_start_screen()
        self.__program_info_screen = self.__create_program_info_screen()
        self.__help_screen = self.__create_help_screen()
        self.__about_developer_screen = self.__create_info_about_developer_screen()
        self.__settings_screen = self.__create_settings_screen()
