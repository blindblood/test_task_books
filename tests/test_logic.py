import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from books_manager import BooksManager
from models import Book, BookStatus


class TestLogic(unittest.TestCase):
    def setUp(self):

        self.data_file = 'test_json.json'
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

        self.books_manager = BooksManager(self.data_file)

        book_id = self.books_manager.last_book_id + 1
        self.book1 = Book(book_id, "The Great Gatsby", "F. Scott Fitzgerald", 1925, BookStatus.AVAILABLE)
        self.books_manager.add_book(self.book1)

        book_id = self.books_manager.last_book_id + 1
        self.book2 = Book(book_id, "Tender Is the Night", "F. Scott Fitzgerald",1934, BookStatus.AVAILABLE)
        self.books_manager.add_book(self.book2)

        book_id = self.books_manager.last_book_id + 1
        self.book3 = Book(book_id, "Moby Dick", "Herman Melville",1925, BookStatus.AVAILABLE)
        self.books_manager.add_book(self.book3)

        self.books_number = len(self.books_manager._load_books())


    def tearDown(self):
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    def test_add(self):
        book_id = self.books_manager.last_book_id + 1
        book1 = Book(book_id, "1984", "George Orwell", 1949, BookStatus.AVAILABLE)

        self.books_manager.add_book(book1)
        books_number = len(self.books_manager._load_books())
        self.assertEqual(self.books_number+1,books_number)
        book_id = self.books_manager.last_book_id + 1

        book2 = Book(book_id, "To Kill a Mockingbird", "Harper Lee", 1960, BookStatus.AVAILABLE)
        self.books_manager.add_book(book2)
        books_number = len(self.books_manager._load_books())
        self.assertEqual(self.books_number+2,books_number)

    def test_delete(self):
        book_id = self.books_manager.last_book_id + 1
        book1 = Book(book_id, "1984", "George Orwell", 1949, BookStatus.AVAILABLE)
        self.books_manager.add_book(book1)

        self.books_manager.remove_book(book_id)
        books_number = len(self.books_manager._load_books())
        self.assertEqual(self.books_number,books_number)


        with self.assertRaises(ValueError) as context:
            self.books_manager.remove_book(book_id)

        self.assertEqual(f"Книга с ID {book_id} не найдена",str(context.exception))


    def test_search(self):
        searched_books=self.books_manager.search_books('author',"F. Scott Fitzgerald")

        self.assertListEqual([self.book1,self.book2],searched_books)

        searched_books=self.books_manager.search_books('title',"Moby Dick")
        self.assertListEqual([self.book3],searched_books)

        searched_books=self.books_manager.search_books('year',str(1925))
        self.assertListEqual([self.book1,self.book3],searched_books)

    def test_status_update(self):
        self.books_manager.update_status(self.book1.id,BookStatus.ISSUED)
        self.assertEqual(BookStatus.ISSUED,self.book1.status)
        self.books_manager.update_status(self.book1.id,BookStatus.ISSUED)
        self.assertEqual(BookStatus.ISSUED,self.book1.status)

        self.books_manager.update_status(self.book1.id,BookStatus.AVAILABLE)
        self.assertEqual(BookStatus.AVAILABLE,self.book1.status)
        self.books_manager.update_status(self.book1.id,BookStatus.AVAILABLE)
        self.assertEqual(BookStatus.AVAILABLE,self.book1.status)

        book_id=99999
        with self.assertRaises(ValueError) as context:
            self.books_manager.update_status(book_id,BookStatus.AVAILABLE)

        self.assertEqual(f"Книга с ID {book_id} не найдена",str(context.exception))

if __name__ == "__main__":
    unittest.main()
