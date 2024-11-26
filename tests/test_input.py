import os
import sys
import unittest
from io import StringIO
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import main
from books_manager import BooksManager
from models import Book, BookStatus


class TestMainInputOutput(unittest.TestCase):

    def setUp(self):
        self.fake_input = StringIO()
        self.fake_output = StringIO()
        sys.stdin = self.fake_input
        sys.stdout = self.fake_output

        self.data_file = 'test_json.json'

        books_manager = BooksManager(self.data_file)

        book_id = books_manager.last_book_id + 1
        self.book1 = Book(book_id, "The Great Gatsby", "F. Scott Fitzgerald", 1925, BookStatus.AVAILABLE)
        books_manager.add_book(self.book1)

        book_id = books_manager.last_book_id + 1
        self.book2 = Book(book_id, "Tender Is the Night", "F. Scott Fitzgerald", 1934, BookStatus.AVAILABLE)
        books_manager.add_book(self.book2)

        book_id = books_manager.last_book_id + 1
        self.book3 = Book(book_id, "Moby Dick", "Herman Melville", 1925, BookStatus.AVAILABLE)
        books_manager.add_book(self.book3)

        self.books_number = len(books_manager._load_books())

    def tearDown(self):
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

        # sys.stdin = sys.__stdin__
        # sys.stdout = sys.__stdout__

    def test_add(self):
        input_data = ["1\n", "Название\n", "Автор\n", "INVALID_DATA\n""20002\n" "2000\n"]
        self.fake_input.writelines(input_data)
        self.fake_input.write("2\n")
        self.fake_input.seek(0)

        main(self.data_file)

        output = self.fake_output.getvalue()
        output = output.strip().splitlines()

        expected_output = [
            "Ошибка",
            "Введите число от 1 до 2024",
            "Ошибка",
            "Введите число от 1 до 2024",
        ]
        self.assertEqual(expected_output, output[-8:-4])

        expected_output = "Книга Название успешно добавлена"
        self.assertEqual(expected_output, output[-4])

        books_manager = BooksManager(self.data_file)
        self.assertEqual(self.books_number + 1, len(books_manager.books))

    def test_delete(self):
        book_id = self.book1.id
        input_data = ["2\n", "INVALID_DATA\n", "\n", f"{book_id}\n"]
        self.fake_input.writelines(input_data)
        self.fake_input.write("2\n")
        self.fake_input.seek(0)

        main(self.data_file)

        output = self.fake_output.getvalue()
        output = output.strip().splitlines()

        expected_output = [
            "Ошибка",
            "Введите число",
            "Ошибка",
            "Введите число",
        ]
        self.assertEqual(expected_output, output[-8:-4])

        expected_output = f"Книга с ID={book_id} успешно удалена"
        self.assertEqual(expected_output, output[-4])

        books_manager = BooksManager(self.data_file)
        self.assertEqual(self.books_number - 1, len(books_manager.books))

    def test_search(self):
        input_data = ["3\n", "INVALID_DATA\n", "1\n", "Moby Dick\n"]
        self.fake_input.writelines(input_data)

        input_data = ["1\n", "3\n", "2\n", "F. Scott Fitzgerald\n"]
        self.fake_input.writelines(input_data)

        input_data = ["1\n", "3\n", "3\n", "1925\n"]
        self.fake_input.writelines(input_data)

        self.fake_input.write("2\n")
        self.fake_input.seek(0)

        main(self.data_file)
        #
        output = self.fake_output.getvalue()
        output = output.strip().splitlines()
        #
        expected_output = [
            "Ошибка",
            "Введите число от 1 до 3",
        ]
        self.assertEqual(expected_output, output[11:13])
        #
        # check title
        expected_output = [
            "Количество найденных книг: 1",
            str(self.book3),
        ]
        self.assertEqual(expected_output, output[14:16])
        #
        # check author
        expected_output = [
            "Количество найденных книг: 2",
            str(self.book1),
            str(self.book2),
        ]
        self.assertEqual(expected_output, output[31:34])

        # check year
        expected_output = [
            "Количество найденных книг: 2",
            str(self.book1),
            str(self.book3),
        ]
        self.assertEqual(expected_output, output[49:52])

    def test_display_all(self):
        input_data = ["4\n"]
        self.fake_input.writelines(input_data)

        self.fake_input.write("2\n")
        self.fake_input.seek(0)

        main(self.data_file)

        output = self.fake_output.getvalue()
        output = output.strip().splitlines()

        expected_output = [
            str(self.book1),
            str(self.book2),
            str(self.book3),
        ]
        self.assertEqual(expected_output, output[-6:-3])

    def test_status_update(self):
        book_id = self.book1.id
        input_data = ["5\n", f'INVALID_DATA\n', f'{book_id}\n', "2\n"]
        self.fake_input.writelines(input_data)
        #wrong id
        input_data = ["1\n", "5\n",f'99999\n',"2\n"]
        self.fake_input.writelines(input_data)

        self.fake_input.write("2\n")
        self.fake_input.seek(0)

        main(self.data_file)

        output = self.fake_output.getvalue()
        output = output.strip().splitlines()

        expected_output = [
            "Ошибка",
            "Введите число",
        ]
        self.assertEqual(expected_output, output[8:10])

        expected_output = [
            "Статус книги с ID 1 обновлен на Выдана"
        ]
        self.assertEqual(expected_output, output[13:14])

        #wrong id
        expected_output = [
            "Книга с ID 99999 не найдена"
        ]
        self.assertEqual(expected_output, output[28:29])

        books_manager = BooksManager(self.data_file)
        new_book_status = books_manager.books[book_id].status
        self.assertEqual(BookStatus.ISSUED, new_book_status)


if __name__ == "__main__":
    unittest.main()
