import sqlite3
from sqlite3 import Error


class DB:
    def __init__(self):
        self._connection = self._create_connection()
        create_books_table = """
        CREATE TABLE IF NOT EXISTS books (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          author TEXT NOT NULL,
          year INTEGER,
          status TEXT,
          isbn INTEGER
        );
        """
        create_readers_table = """
        CREATE TABLE IF NOT EXISTS readers (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          surname TEXT NOT NULL,
          birth TEXT NOT NULL,
          sex TEXT NOT NULL,
          nat_id TEXT NOT NULL
        );
        """

        create_borrowings_table = """
        CREATE TABLE IF NOT EXISTS borrows (
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          book_id INTEGER NOT NULL,
          reader_id INTEGER NOT NULL,
          borrow_date TEXT NOT NULL,
          return_date TEXT NOT NULL,
          returned TEXT,
          FOREIGN KEY (book_id) REFERENCES books (id),
          FOREIGN KEY (reader_id) REFERENCES readers (id)
        );
        """

        self.execute_query(create_books_table)
        self.execute_query(create_readers_table)
        self.execute_query(create_borrowings_table)

    def _create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect('db.sqlite')
            print("Connected")
        except Error as e:
            print(f"{e} occurred")
        return connection

    def execute_query(self, query):
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            self._connection.commit()
            print("Query executed")
        except Error as e:
            print(f"{e} occurred")

    def execute_read_query(self, query):
        cursor = self._connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"{e} occurred")
