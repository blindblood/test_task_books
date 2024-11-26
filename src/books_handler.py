from datetime import datetime
from typing import Callable, Any

from books_manager import BooksManager
from models import Book, BookStatus


class BooksHandler:
    """
    Класс для обработки ввода пользователя и взаимодействия с BooksManager.

    Атрибуты:
    - books_manager: Экземпляр класса BooksManager.
    - menu: Доступные пункты меню для пользователя.

    """

    def __init__(self, books_manager: BooksManager):
        self.books_manager = books_manager

        self.menu = (
            ("Добавить книгу", self.handle_add_book),
            ("Удалить книгу", self.handle_remove_book),
            ("Искать книгу", self.handle_search_book),
            ("Показать все книги", self.handle_display_books),
            ("Изменить статус книги", self.handle_update_status),
            ("Выход", None),
        )

        self.current_year = datetime.now().year
        self.menu_length = len(self.menu)

    def validate_input(self, promt: str = "", to_type: type = str, condition: Callable[[Any], Any] = lambda x: x,
                       error_message="Неверные данные") -> Any:
        """
        Валидирует пользовательский ввод с помощью заданных параметров.

        Функция повторно запрашивает ввод от пользователя, пока введённые данные не будут удовлетворять
        указанным условиям и типу.

        Параметры:
        - prompt (str): Сообщение, которое будет выведено перед запросом ввода (по умолчанию пустое сообщение).
        - to_type (type): Тип, в который нужно преобразовать введённые данные (по умолчанию str).
        - condition (Callable[[Any], Any]): Функция, которая проверяет валидность введённых данных.
        - error_message (str): Сообщение об ошибке, которое будет отображаться при некорректных данных (по умолчанию "Неверные данные").

        Возвращает:
        - Обработанные данные после преобразования в указанный тип и проверки с условием.

        """

        if promt: print(promt)

        while True:
            try:
                input_data = input()
                input_data = to_type(input_data.strip())
                if not condition(input_data):
                    raise ValueError
                return input_data
            except Exception as error:
                # print(error)# delete
                print(f'Ошибка\n{error_message}')

    def handle_add_book(self) -> None:
        """
        Обрабатывает добавление новой книги.
        """
        title = input("Введите название книги:\n").title().strip()
        author = input("Введите автора книги:\n").title().strip()
        year = self.validate_input("Введите год издания книги:", int, lambda x: 1 <= x <= self.current_year,
                                   f"Введите число от 1 до {self.current_year}")

        book_id = self.books_manager.last_book_id + 1
        book = Book(book_id, title, author, year, BookStatus.AVAILABLE)
        self.books_manager.add_book(book)
        print(f"Книга {title} успешно добавлена")

    def handle_remove_book(self) -> None:
        """
        Обрабатывает удаление книги по ID.
        """
        book_id = self.validate_input("Введите ID книги ", int, error_message="Введите число")
        try:
            self.books_manager.remove_book(book_id)
            print(f"Книга с ID={book_id} успешно удалена")

        except ValueError as error:
            print(error)

    def handle_search_book(self) -> None:
        """
        Обрабатывает поиск книги по заданному фильтру.
        """
        filter_options = (
            ("Название", "title"),
            ("Автор", "author"),
            ("Год издания", "year"),
        )
        filter_options_len = len(filter_options)

        print("Выберите поле для фильтрации")
        for index, (name, _) in enumerate(filter_options, start=1):
            print(f"{index}. {name}")

        choice_number = self.validate_input("", int, lambda x: 1 <= x <= filter_options_len,
                                            f"Введите число от 1 до {filter_options_len}")

        _, filter_field = filter_options[choice_number - 1]

        query = input("Введите запрос для поиска:\n").lower().strip()
        found_books = self.books_manager.search_books(filter_field, query)
        if not found_books:
            print("По вашему запросу книги не найдены")
            return

        print(f'Количество найденных книг: {len(found_books)}')
        for book in found_books:
            print(book)

    def handle_display_books(self) -> None:
        """
        Отображает все книги.
        """
        books = self.books_manager.books.values()
        if not books:
            print("Нет добавленных книг")
            return
        for book in books:
            print(book)

    def handle_update_status(self) -> None:
        """
        Обрабатывает обновление статуса книги.
        """
        book_id = self.validate_input("Введите ID книги ", int, error_message="Введите число")

        print("Выберите новый статус")
        for index, book_status in enumerate(BookStatus, start=1):
            print(f"{index}. {book_status.value}")

        filter_options_len = len(BookStatus)
        choice_number = self.validate_input("", int, lambda x: 1 <= x <= filter_options_len,
                                            f"Введите число от 1 до {filter_options_len}")

        new_status = list(BookStatus)[choice_number - 1]
        try:
            self.books_manager.update_status(book_id, new_status)
            print(f"Статус книги с ID {book_id} обновлен на {new_status.value}")

        except ValueError as error:
            print(error)

    def display_menu(self) -> None:
        """
        Отображает меню выбора для пользователя.
        """
        print("Меню:")
        for index, (item, _) in enumerate(self.menu, start=1):
            print(f"{index}. {item}")

    def run(self) -> None:
        """
        Запускает главный цикл программы.
        """
        self.display_menu()
        while True:
            choice_number = self.validate_input("", int, lambda x: 1 <= x <= self.menu_length,
                                                f"Введите число от 1 до {self.menu_length}")
            if choice_number == self.menu_length:
                break
            _, action = self.menu[choice_number - 1]
            action()

            choice_number = self.validate_input("Продолжить работу:\n1. Да\n2. Нет", int, lambda x: 1 <= x <= 2,
                                                f"Введите число от 1 до 2")
            if choice_number == 2:
                break
            self.display_menu()
