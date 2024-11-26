# Book Management System

Проект "Book Management System" — это консольное приложение, предназначенное для управления книгами в библиотеке. Оно предоставляет возможность добавлять, удалять, искать книги и изменять их статус. Приложение использует простой текстовый интерфейс для взаимодействия с пользователем.

## Описание функционала
 Весь процесс взаимодействия с пользователем происходит через меню с числовым выбором. 

Меню:
1. Добавить книгу
2. Удалить книгу
3. Искать книгу
4. Показать все книги
5. Изменить статус книги
6. Выход

- Добавить книгу: При выборе пункта "1. Добавить книгу", пользователю будет предложено ввести: название книги, имя автора год издания.


- Удалить книгу: При выборе пункта "2. Удалить книгу", пользователю нужно ввести ID книги, которую нужно удалить.


- Искать книгу: При выборе пункта "3. Искать книгу", пользователь может выбрать критерий поиска (по названию, автору или году издания) и ввести строку для поиска. Результат будет выведен в виде списка найденных книг:


- Показать все книги: При выборе пункта "4. Показать все книги", приложение отобразит список всех добавленных книг с полной информацией:


- Изменить статус книги: "5. Изменить статус книги", пользователь вводит ID книги и  выбирает новый статус: В наличии или Выдана.
## Структура проекта

Проект состоит из нескольких файлов:
- `models.py`: содержит описание классов `Book` и `BookStatus` для представления книг и их статусов.
- `books_manager.py`: реализует логику работы с книгами, включая добавление, изменение статуса, удаление и поиск.
- `books_handler.py`: интерфейс взаимодействия с пользователем, обрабатывает команды и ввод.
- `main.py`: основной файл для запуска приложения.

