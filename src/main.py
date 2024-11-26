import os
import sys
from io import StringIO
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from books_handler import BooksHandler
from books_manager import BooksManager




def main(file_path='books_data.json'):
    books_manager = BooksManager(file_path)
    books_handler = BooksHandler(books_manager)
    books_handler.run()


if __name__ == '__main__':
    main()
