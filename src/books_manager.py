import json
import os

from models import Book, BookStatus


class BooksManager:
    """
    Класс для управления книгами.

    Атрибуты:
    - data_file: Путь к файлу данных о книгах.
    - books: Словарь книг, где ключ - это id книги.
    - last_book_id: Последний использованный ID книги.
    """

    def __init__(self, data_file='books_data.json'):
        self.data_file = data_file
        self._books = self._load_books()
        self._last_book_id = max(self._books.keys(), default=0)

    @property
    def last_book_id(self) -> int:
        return self._last_book_id

    @property
    def books(self) -> dict[int, Book]:
        return self._books

    def _load_books(self) -> dict[int, Book]:
        """
        Загружает книги из файла данных.

        Если файл не существует или поврежден, создается пустой список.
        """
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump([], file)
        books = {}
        try:
            with open(self.data_file, mode='r', encoding='utf-8') as file:
                data = json.load(file)
                books = {book['id']: Book.from_dict(book) for book in data}
        except json.JSONDecodeError as error:
            print(f"Ошибка при чтении файла {self.data_file}: некорректный формат JSON")
        except FileNotFoundError:
            print(f"Файл {self.data_file} не найден")
        finally:
            return books

    def _save_books(self) -> None:
        with open(self.data_file, mode='w', encoding='utf-8') as file:
            data = [book.to_dict() for book in self._books.values()]
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.flush()

    def add_book(self, book: Book) -> None:
        """
        Добавляет книгу в систему.
        """
        self._books[book.id] = book
        self._last_book_id += 1
        self._save_books()

    def remove_book(self, book_id: int) -> None:
        """
        Удаляет книгу по ID.
        """
        if book_id not in self._books:
            raise ValueError(f"Книга с ID {book_id} не найдена")

        del self._books[book_id]
        self._save_books()

    def search_books(self, filter_field: str, query: str) -> list[Book]:
        """
        Ищет книги по заданному фильтру.

        Параметры:
        - filter_field (str): Поле для фильтрации (title, author или year).
        - query (str): Запрос для поиска.
        """
        query = query.lower()
        result = [
            book for book in self._books.values()
            if str(getattr(book, filter_field)).lower() == query
        ]
        return result

    def update_status(self, book_id: int, new_status: BookStatus):
        """
        Обновляет статус книги.
        """
        if book_id not in self._books:
            raise ValueError(f"Книга с ID {book_id} не найдена")

        if self._books[book_id].status != new_status:
            self._books[book_id].status = new_status
            self._save_books()
