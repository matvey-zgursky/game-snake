"""
Модуль содержит абстрактный класс Screen, имеющий 
функционал переключения экрана и создания его виджетов.

imports:
    ABC: Чтобы сделать класс Screen абстрактным.
    abstractmethod: Для обозначения абстрактого метода.
"""
from abc import ABC, abstractmethod


class Screen(ABC):
    """Предназначен для наследования другими экранами."""
    @abstractmethod
    def create(self) -> None:
        """Создает виджеты экрана."""
        pass

    def hide(self) -> None:
        """Скрывает экран."""
        self.frame.pack_forget()

    def show(self) -> None:
        """Показывает экран."""
        self.frame.pack(expand=True)
