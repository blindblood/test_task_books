from enum import Enum


class BookStatus(Enum):
    """
    Перечисление для статусов книг.

    AVAILABLE: Книга в наличии.
    ISSUED: Книга выдана.
    """
    AVAILABLE = "В наличии"
    ISSUED = "Выдана"

class Book:
    """
    Класс для представления книги.

    Атрибуты:
    - id: Уникальный идентификатор книги.
    - title: Название книги.
    - author: Автор книги.
    - year: Год издания книги.
    - status: Статус книги (BookStatus).
    """
    def __init__(self, id: int, title: str, author: str, year: int, status: BookStatus = BookStatus.AVAILABLE) -> object:
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls,data: dict):
        return cls(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=BookStatus(data["status"])
        )


    def __str__(self):
        return f'ID: {self.id}, Название: {self.title}, Автор:{self.author}, Год издания: {self.year} , Статус: {self.status.value}'

