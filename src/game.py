"""
Модуль отвечает за инициализацию и управление главного окна игры.

Модуль включает класс с методами для запуска игры и выхода из нее.

Classes:
    Game: Для инициализации главного окна игры, управление им и создание игровых экранов.

imports:
    tkinter: Для инициализации главного окна игры.
    ScreensControl: Для создания игровых экранов.
"""
import tkinter as tk

from screens.screens_control import ScreensControl


class Game:
    """
    Отвечает за инициализацию и управление главного окна игры, а также за создание её экранов.
    
    Attributes:
        root (tk.Tk): Главное окно приложения.
        scr_control (ScreensControl): Управление игровыми экранами.
    """
    def __init__(self) -> None:
        """Инициализирует главное окно игры и создает игровые экраны."""
        self.root = tk.Tk()
        self.root.title('Змейка')
        self.root.resizable(False, False)
        self.root.geometry('620x660')

        scr_control = ScreensControl(master=self.root, quit_callback=self.quit_)
        scr_control.create_screens()
        
    def quit_(self) -> None:
        """Завершить работу приложения."""
        self.root.quit()

    def run(self) -> None:
        """Запустить главный цикл обработки событий окна приложения."""
        self.root.mainloop()
