import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from books_manager import BooksManager
from models import Book, BookStatus


class TestLogic(unittest.TestCase):
    def setUp(self):
        """
        Подготовка перед каждым тестом:
        - Создается временный файл данных.
        - Инициализируется объект BooksManager.
        - Добавляются три книги для тестирования функциональности.
        """
        self.data_file = 'test_json.json'
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

        self.books_manager = BooksManager(self.data_file)

        # Добавление первой книги
        book_id = self.books_manager.last_book_id + 1
        self.book1 = Book(book_id, "The Great Gatsby", "F. Scott Fitzgerald", 1925, BookStatus.AVAILABLE)
        self.books_manager.add_book(self.book1)

        # Добавление второй книги
        book_id = self.books_manager.last_book_id + 1
        self.book2 = Book(book_id, "Tender Is the Night", "F. Scott Fitzgerald",1934, BookStatus.AVAILABLE)
        self.books_manager.add_book(self.book2)

        # Добавление третьей книги
        book_id = self.books_manager.last_book_id + 1
        self.book3 = Book(book_id, "Moby Dick", "Herman Melville",1925, BookStatus.AVAILABLE)
        self.books_manager.add_book(self.book3)

        # Количество книг в системе
        self.books_number = len(self.books_manager._load_books())


    def tearDown(self):
        """
        Очистка после каждого теста:
        - Удаляется временный файл данных.
        """
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    def test_add(self):
        """
        Тестирование функции добавления книг.
        - Проверяется корректность увеличения количества книг.
        """
        book_id = self.books_manager.last_book_id + 1
        book1 = Book(book_id, "1984", "George Orwell", 1949, BookStatus.AVAILABLE)

        # Добавление первой книги
        self.books_manager.add_book(book1)
        books_number = len(self.books_manager._load_books())
        self.assertEqual(self.books_number+1,books_number)
        book_id = self.books_manager.last_book_id + 1

        # Добавление второй книги
        book2 = Book(book_id, "To Kill a Mockingbird", "Harper Lee", 1960, BookStatus.AVAILABLE)
        self.books_manager.add_book(book2)
        books_number = len(self.books_manager._load_books())
        self.assertEqual(self.books_number+2,books_number)

    def test_delete(self):
        """
        Тестирование функции удаления книг.
        - Проверяется корректное удаление книги.
        - Проверяется обработка ошибки при удалении несуществующей книги.
        """
        book_id = self.books_manager.last_book_id + 1
        book1 = Book(book_id, "1984", "George Orwell", 1949, BookStatus.AVAILABLE)
        self.books_manager.add_book(book1)

        # Удаление книги
        self.books_manager.remove_book(book_id)
        books_number = len(self.books_manager._load_books())
        self.assertEqual(self.books_number,books_number)

        # Попытка удаления несуществующей книги
        with self.assertRaises(ValueError) as context:
            self.books_manager.remove_book(book_id)

        self.assertEqual(f"Книга с ID {book_id} не найдена",str(context.exception))


    def test_search(self):
        """
        Тестирование функции поиска книг.
        - Проверяется поиск по автору.
        - Проверяется поиск по названию.
        - Проверяется поиск по году издания.
        """

        # Поиск по автору
        searched_books=self.books_manager.search_books('author',"F. Scott Fitzgerald")
        self.assertListEqual([self.book1,self.book2],searched_books)

        # Поиск по названию
        searched_books=self.books_manager.search_books('title',"Moby Dick")
        self.assertListEqual([self.book3],searched_books)

        # Поиск по году
        searched_books=self.books_manager.search_books('year',str(1925))
        self.assertListEqual([self.book1,self.book3],searched_books)

    def test_status_update(self):
        """
        Тестирование функции обновления статуса книги.
        - Проверяется успешное обновление статуса.
        - Проверяется обработка ошибки при обновлении статуса несуществующей книги.
        """

        # Изменение статуса книги
        self.books_manager.update_status(self.book1.id,BookStatus.ISSUED)
        self.assertEqual(BookStatus.ISSUED,self.book1.status)
        self.books_manager.update_status(self.book1.id,BookStatus.ISSUED)
        self.assertEqual(BookStatus.ISSUED,self.book1.status)

        # Изменение статуса книги
        self.books_manager.update_status(self.book1.id,BookStatus.AVAILABLE)
        self.assertEqual(BookStatus.AVAILABLE,self.book1.status)
        self.books_manager.update_status(self.book1.id,BookStatus.AVAILABLE)
        self.assertEqual(BookStatus.AVAILABLE,self.book1.status)

        # Попытка обновления статуса несуществующей книги
        book_id=99999
        with self.assertRaises(ValueError) as context:
            self.books_manager.update_status(book_id,BookStatus.AVAILABLE)

        self.assertEqual(f"Книга с ID {book_id} не найдена",str(context.exception))

if __name__ == "__main__":
    unittest.main()
