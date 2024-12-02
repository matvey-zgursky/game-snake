"""
Главный модуль, предназначен для запуска игры.

Funcions:
    main: Осуществляет запуск игры

Imports:
    Game: Для инициализации и запуска игры.
"""
from game import Game


def main() -> None:
    """Главная функция для инициализации и запуска игры."""
    try:
        game = Game()
        game.run()
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
