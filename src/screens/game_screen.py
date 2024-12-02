"""
Модуль отвечает за игровой экран.

Classes:
    GameCanvas: Содержит создание, обновление, постановка на паузу, 
    перезагрузка игрового холста, управление змейкой, инициализация 
    игровых объектов, их отрисовка и отработка коллизий.
    StatusBar: Содержит создание, обновление игровых параметров статус бара.
    GameScreen: Содержит функционал инициализации экрана игрового экрана
    и создания его виджетов, а также старта игры, обновления статус бара, 
    обработчика появления экрана проигрыша, переопределенные методы 
    родительского класса его переключения.

Imports:
    tkinter: Для написания аннотации типа аргумента master всех классов.
    Callable: Для написания аннотации типа аргумента buttons всех классов.
    override: Для определения переопределенных методов GameScreen.

    Image, ImageTk: Для загрузки изображения жизней.

    Screen: Является родительским классом класса StartScreen.
    Snake, Food: Для создания и взаимодействия в классе GameCanvas.
"""
import tkinter as tk
from typing import Callable, override

from PIL import Image, ImageTk

from screens.screen import Screen
from canvas_objects.snake import Snake
from canvas_objects.food import Food


class GameCanvas:
    """
    Содержит функционал игрового процесса: создание, обновление,
    постановка на паузу, перезагрузка игрового холста, управление 
    змейкой, инициализация игровых объектов, их отрисовка и 
    отработка коллизий.

    Attributes:
        master (Frame): Родительский экран.
    """
    def __init__(
        self,
        *,
        master: tk.Frame,
        update_status_bar_callback: Callable[[int, int], None],
        game_over_callback: Callable[[int], None],
        settings: dict[str, int | str]
        ) -> None:
        """
        Инициализирует игровой холст.

        Args:
            master (Frame): Родительский экран.
            game_over_callback (Callable[[int], None]): Возвращаемая функция проигрыша.
            settings (dict[str, int | str]): Настройки игры.
        """
        self.master = master

        self.__CANVAS_WIDTH = 600
        self.__CANVAS_HEIGTH = 600
        self.__CELL_SIZE = 20

        self.__score = 0
        self.__lives = 3

        self.__game_over = False
        self.__after_id = None

        self.__update_status_bar_callback = update_status_bar_callback
        self.__game_over_callback = game_over_callback

        self.__settings = settings
        __snake_speed = self.__settings.get('snake speed', 10) * 10
        self.__move_delay = 200 - __snake_speed

    def stop(self) -> None:
        """Останавливает игровой холст."""
        if self.__after_id is not None:
            self.master.after_cancel(self.__after_id)
            self.__after_id = None
        self.__game_over = True

    def handle_button_presses(self, event: tk.Event) -> None:
        """
        Обрабатывает нажатие кнопки.
        
        Returns:
            event (tk.Event): Игровые события.
        """
        key = event.keysym.lower()
        key_directions = {'w': 'Up', 'a': 'Left', 's': 'Down', 'd': 'Right'}
        if key in key_directions:
            new_direction = key_directions[key]
            self.__snake.change_direction(new_direction)

    def __reset_game_parameters(self) -> None:
        """Перезапускает игровые параметры и показатели."""
        self.__score = 0
        self.__lives = 3
        self.__game_over = False
        __snake_speed = self.__settings.get('snake speed', 10) * 10
        self.__move_delay = 200 - __snake_speed
        self.__update_status_bar_callback(self.__score, self.__lives)

    def __init_snake(self) -> Snake:
        """
        Инициализирует змейку.

        Returns:
            Snake: Экземпляр змейки.
        """
        head_x = (
            self.__CANVAS_WIDTH // self.__CELL_SIZE
            ) // 2 * self.__CELL_SIZE
        head_y = (
            self.__CANVAS_HEIGTH // self.__CELL_SIZE
            ) // 2 * self.__CELL_SIZE
        initial_length = self.__settings.get('snake length', 3)
        initial_positions = []
        for i in range(initial_length):
            initial_positions.append((head_x - i * self.__CELL_SIZE, head_y))

        initial_direction = 'Right'
        snake = Snake(
            segment_positions=initial_positions,
            initial_direction=initial_direction
            )

        return snake

    def __init_food(self) -> Food:
        """
        Инициализирует еду.

        Returns:
            Food: Экземпляр еды.
        """
        snake_positions = self.__snake.get_segment_positions()
        food = Food(
            canvas_width=self.__CANVAS_WIDTH,
            canvas_heigth=self.__CANVAS_HEIGTH,
            cell_size=self.__CELL_SIZE,
            )
        food.set_new_position(snake_positions=snake_positions)

        return food

    def __init_game_objects(self) -> None:
        """Инициализует игровые объекты."""
        self.__snake = self.__init_snake()
        self.__food = self.__init_food()

    def __reset_snake(self) -> None:
        """Пересоздает змейку."""
        self.__snake = self.__init_snake()
        __snake_speed = self.__settings.get('snake speed', 10) * 10
        self.__move_delay = 200 - __snake_speed

    def __handle_collision_with_walls(self) -> None:
        """Отрабатывает коллизию змейки со стеной."""
        head_x, head_y = self.__snake.get_head_position()
        if head_x < 0 or head_y < 0 or \
            head_x >= self.__CANVAS_WIDTH or head_y >= self.__CANVAS_HEIGTH:
            self.__lives -= 1
            self.__update_status_bar_callback(self.__score, self.__lives)
            if self.__lives > 0:
                self.__reset_snake()
            else:
                previous_snake_position = self.__snake.get_previous_position()
                self.__snake.return_snake_to_previous_position(
                    prev_position=previous_snake_position
                    )
                self.__game_over_callback(self.__score)
                self.__game_over = True

    def __handle_collision_with_food(self) -> None:
        """Отрабатывает коллизию змейки с едой."""
        head_position = self.__snake.get_head_position()
        snake_positions = self.__snake.get_segment_positions()
        food_position = self.__food.get_position()
        if head_position == food_position:
            self.__snake.add_segment_to_end()
            self.__score += 1
            self.__update_status_bar_callback(self.__score, self.__lives)
            self.__food.set_new_position(snake_positions=snake_positions)
            self.__move_delay = max(10, self.__move_delay - 2)

    def __handle_collision_with_self(self) -> None:
        """Отрабатывает коллизию змейки самой с собой."""
        snake_positions = self.__snake.get_segment_positions()
        head_position = self.__snake.get_head_position()
        if head_position in snake_positions[1:]:
            self.__lives -= 1
            self.__update_status_bar_callback(self.__score, self.__lives)
            if self.__lives > 0:
                self.__reset_snake()
            else:
                previous_snake_position = self.__snake.get_previous_position()
                self.__snake.return_snake_to_previous_position(
                    prev_position=previous_snake_position
                    )
                self.__game_over_callback(self.__score)
                self.__game_over = True

    def __handle_collisions(self) -> None:
        """Отрабатывает коллизии игровых объектов."""
        self.__handle_collision_with_walls()
        self.__handle_collision_with_food()
        self.__handle_collision_with_self()

    def __draw_snake(self) -> None:
        """Отрисовывает змейку."""
        snake_positions = self.__snake.get_segment_positions()
        snake_color = self.__settings.get('snake color', 'green')
        for x, y in snake_positions:
            self.canvas.create_rectangle(
                x,
                y,
                x + self.__CELL_SIZE,
                y + self.__CELL_SIZE,
                fill=snake_color
                )

    def __draw_food(self) -> None:
        """Отрисовывает еду."""
        x, y = self.__food.get_position()
        self.canvas.create_oval(
            x, y, x + self.__CELL_SIZE, y + self.__CELL_SIZE, fill='red'
            )

    def __update_objects(self) -> None:
        """Обновляет отрисовку игровых объектов."""
        self.canvas.delete(tk.ALL)
        self.__draw_snake()
        self.__draw_food()

    def __update(self) -> None:
        """Обновляет игровой холст."""
        if self.__game_over:
            return

        self.__snake.move()
        self.__handle_collisions()
        self.__update_objects()
        self.__after_id = self.master.after(
            self.__move_delay, self.__update
            )

    def start(self) -> None:
        """Запускает игровой процесс."""
        self.__reset_game_parameters()
        self.__init_game_objects()
        self.__update_objects()
        self.__after_id = self.master.after(100, self.__update)

    def create(self) -> None:
        """Создание игрового холста."""
        self.canvas = tk.Canvas(
            self.master,
            bg=self.__settings.get('canvas color', 'black'),
            width=self.__CANVAS_WIDTH,
            height=self.__CANVAS_HEIGTH
            )
        self.canvas.pack()


class StatusBar:
    """
    Содержит функционал статус бара: создание, обновление 
    игровых параметров.

    Attributes:
        master (Tk): Родительский экран.
        frame (Frame): Сам статус бар.
    """
    def __init__(
        self,
        *,
        master: tk.Frame,
        buttons: dict[str, Callable[[], None]],
        initial_score: int,
        record_score: int,
        lives: int
        ) -> None:
        """
        Инициализирует статус бар  и привязывает его к родительскому окну.

        Args:
            master (Frame): Родительское окно.
            buttons (dict[str, Callable[[], None]]): Словарь кнопок с \
                их названиями и функциями обратного вызова.
            initial_score (int): Стартовое количество игровых очков.
            record_score (int): Рекордное количетсво очков.
            lives (int): Количество жизней.
        """
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.TOP, fill=tk.X)

        self.__FONT = ('Arial', 16)

        self.__buttons = buttons

        self.__initial_score = initial_score
        self.__record_score = record_score
        self.__lives = lives

        self.__heart_photo = self.__load_hearts()

    def __delete_heart(self) -> None:
        """Удаляет жизнь."""
        for heart_label in self.heart_labels:
            heart_label.pack_forget()
        self.heart_labels.clear()

    def __add_hearts(self, lives: int) -> None:
        """
        Создает жизни.

        Args:
            lives (int): Количество жизней. 
        """
        for _ in range(lives):
            heart_label = tk.Label(self.hearts_frame, image=self.__heart_photo)
            heart_label.pack(side=tk.LEFT)
            self.heart_labels.append(heart_label)

    def _update_result_label(
        self, score: int, record_score: int, lives: int
        ) -> None:
        """
        Обновляет виджеты игровых параметров.
        
        Args:
            score (int): Количетсво заработанных очков.
            record_score (int): Рекорд заработанных очков.
            lives (int): Количество жизней.
        """
        self.__score_label.config(text=f'Счет: {score}  ')
        self.__record_label.config(text=f'Рекорд: {record_score}  ')

        self.__delete_heart()
        self.__add_hearts(lives)

    def __create_score(self, master: tk.Frame) -> None:
        """
        Создание виджета заработанных очков.

        Args:
            master (Frame): Родительский виджет.
        """
        self.__score_label = tk.Label(
            master, text=f'Счет: {self.__initial_score}', font=self.__FONT
            )
        self.__score_label.pack(side=tk.LEFT)

    def __create_records(self, master: tk.Frame) -> None:
        """
        Создание виджета рекорда очков.

        Args:
            master (Frame): Родительский виджет.
        """
        self.__record_label = tk.Label(
            master, text=f'  Рекорд: {self.__record_score}', font=self.__FONT
            )
        self.__record_label.pack(side=tk.LEFT)

    def __load_hearts(self) -> ImageTk.PhotoImage:
        """
        Загружает изображение жизни. 
        
        Returns:
            PhotoImage: Изображение жизни.
        """
        image = Image.open(r'./images/heart.png')
        image = image.resize((30, 30))
        photo = ImageTk.PhotoImage(image)

        return photo

    def __create_hearts(self, master: tk.Frame) -> None:
        """
        Создание виджета жизней.

        Args:
            master (Frame): Родительский виджет.
        """
        self.hearts_frame = tk.Frame(master)
        self.hearts_frame.pack(side=tk.LEFT)

        self.heart_labels = []
        for _ in range(self.__lives):
            heart_label = tk.Label(self.hearts_frame, image=self.__heart_photo)
            heart_label.pack(side=tk.LEFT)
            self.heart_labels.append(heart_label)

    def __create_changing_parameters(self) -> None:
        """Создание виджета игровых параметров."""
        parameters_frame = tk.Frame(self.frame)
        parameters_frame.pack(side=tk.LEFT)

        self.__create_score(master=parameters_frame)
        self.__create_records(master=parameters_frame)
        self.__create_hearts(master=parameters_frame)

    def __create_button(self) -> None:
        """Создает кнопки на родительском виджете."""
        for key, value in self.__buttons.items():
            button = tk.Button(
                self.frame,
                text=key,
                font=self.__FONT,
                width=15,
                command=value
                )
            button.pack(side=tk.RIGHT)

    def create(self) -> None:
        """Создание виджетов статус бара."""
        self.__create_changing_parameters()
        self.__create_button()


class GameScreen(Screen):
    """
    Содержит функционал инициализации и создания виджетов экрана, старта игры,
    обновления статус бара, обработчика появления экрана проигрыша. а также 
    переопределенные методы родительского класса его переключения.

    Attributes:
        master (Tk): Родительское окно.
        frame (Frame): Сам экран.
    """
    def __init__(
        self,
        *,
        master: tk.Tk,
        buttons: dict[str, Callable[[], None]],
        game_over_callback: Callable[[int], None],
        record_score: int,
        settings: dict[str, int | str]
        ) -> None:
        """
        Инициализирует экран и привязывает его к родительскому окну.

        Args:
            master (Tk): Родительское окно.
            buttons (dict[str, Callable[[], None]]): Словарь кнопок с \
                их названиями и функциями обратного вызова.
            game_over_callback (Callable[[int], None]): Возвращаемая функция проигрыша.
            record_score (int): Рекорд очков пользователя.
            settings (dict[str, int | str]): Настройки игры.
        """
        self.master = master
        self.frame = tk.Frame(self.master)

        self.__buttons = buttons

        self.__record_score = record_score
        self.__settings = settings

        self.__lives = 3

        self.__game_over_callback = game_over_callback

    def __start_game(self) -> None:
        """Запускает игоровой холст, что приводит к запуску игрового процесса"""
        self.master.bind('<Key>', self.__game_canvas.handle_button_presses)
        self.__game_canvas.start()

    def __create_status_bar(self) -> StatusBar:
        """
        Создает статус бар на экране.
        
        Returns:
            StatusBar: Экземпляр статус бара.
        """
        status_bar = StatusBar(
            master=self.frame,
            buttons=self.__buttons,
            initial_score=0,
            record_score=self.__record_score,
            lives=self.__lives
            )
        status_bar.create()

        return status_bar

    def _update_status_bar(self, score: int, lives: int) -> None:
        """
        Обновляет статус бар.

        Args:
            score (int): Заработанные очки игрока.
            lives (int): Количество жизней.
        """
        if score > self.__record_score:
            self.__record_score = score

        self.__status_bar._update_result_label(
            score, self.__record_score, lives
            )

    @override
    def hide(self) -> None:
        """Скрывает экран."""
        self.frame.pack_forget()
        self.__game_canvas.stop()
        self.master.unbind('<Key>')

    def _handle_game_over(self, score: int) -> None:
        """
        Обрабатывает проигрыш.

        Args:
            score (int): Заработанные очки игрока.
        """
        self.hide()
        self.__game_over_callback(score, self.__record_score)

    def __create_game_canvas(self) -> GameCanvas:
        """
        Создает игровой холст на экране.
        
        Returns:
            GameCanvas: Экземпляр игрового холста
        """
        game_canvas = GameCanvas(
            master=self.frame,
            update_status_bar_callback=self._update_status_bar,
            game_over_callback=self._handle_game_over,
            settings=self.__settings
            )
        game_canvas.create()

        return game_canvas

    def create(self) -> None:
        """Создает виджеты экрана."""
        self.__status_bar = self.__create_status_bar()
        self.__game_canvas = self.__create_game_canvas()

    @override
    def show(self) -> None:
        """Показывает экран."""
        self.frame.pack(expand=True)
        self.__start_game()
