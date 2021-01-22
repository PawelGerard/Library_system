from db import DB
from sqlite3 import Error


class Model:
    def __init__(self):
        print('Model')
        self._db = DB()

    def get_books(self, search):
        books = self._db.execute_read_query(f"SELECT * FROM books WHERE title LIKE '%{search}%'")
        return books

    def get_readers(self, search):
        readers = self._db.execute_read_query(f"SELECT * FROM readers WHERE surname LIKE '%{search}%'")
        return readers

    def get_borrows(self, search):
        statement = f"""
                    SELECT br.id, br.book_id, b.title, b.isbn, r.name || ' ' || r.surname as person, br.borrow_date,
                    br.return_date, br.returned FROM borrows br INNER JOIN books b ON br.book_id=b.id INNER JOIN
                    readers r ON br.reader_id=r.id WHERE b.title LIKE '%{search}%' OR person LIKE '%{search}%';
                    """
        borrows = self._db.execute_read_query(statement)
        return borrows

    def insert_into_books(self, title, author, year, status, isbn):
        statement = f"""
                INSERT INTO books(title, author, year, status, isbn)
                VALUES
                ('{title}', '{author}', {year}, '{status}', {isbn});
                """
        self._db.execute_query(statement)

    def insert_into_readers(self, name, surname, birth, sex, nat_id):
        statement = f"""
                INSERT INTO readers(name, surname, birth, sex, nat_id)
                VALUES
                ('{name}', '{surname}', '{birth}', '{sex}', '{nat_id}');
                """
        self._db.execute_query(statement)

    def insert_into_borrows(self, book_id, reader_id, borrow_date, return_date):
        statement = f"""
                INSERT INTO borrows(book_id, reader_id, borrow_date, return_date)
                VALUES
                ({book_id}, {reader_id}, '{borrow_date}', '{return_date}');
                """
        self._db.execute_query(statement)

    def update_book(self, id_number, title, author, year, status, isbn):
        statement = f"""
                UPDATE books SET
                title = '{title}', author='{author}', year={year}, status='{status}', isbn={isbn}
                WHERE id={id_number};
                """
        self._db.execute_query(statement)

    def update_reader(self, id_number, name, surname, birth, sex, nat_id):
        statement = f"""
                UPDATE readers SET
                name = '{name}', surname='{surname}', birth='{birth}', sex='{sex}', nat_id='{nat_id}'
                WHERE id={id_number};
                """
        self._db.execute_query(statement)

    def update_borrows_returned(self, id_number, returned):
        statement = f"UPDATE borrows SET returned = '{returned}' WHERE id={id_number};"
        self._db.execute_query(statement)

    def update_borrows_return_date(self, id_number, return_date):
        statement = f"UPDATE borrows SET return_date = '{return_date}' WHERE id={id_number};"
        self._db.execute_query(statement)

    def delete_book(self, id_number):
        statement = f"""
                DELETE FROM books
                WHERE id={id_number};
                """
        self._db.execute_query(statement)

    def delete_reader(self, id_number):
        statement = f"""
                DELETE FROM readers
                WHERE id={id_number};
                """
        self._db.execute_query(statement)

    def get_book(self, id):
        statement = f"SELECT * FROM books WHERE id = {id}"
        result = self._db.execute_read_query(statement)
        return result

    def get_reader(self, id):
        statement = f"SELECT * FROM readers WHERE id = {id}"
        result = self._db.execute_read_query(statement)
        return result

    def check_book_status(self, id):
        statement = f"SELECT status FROM books WHERE id = {id}"
        result = self._db.execute_read_query(statement)
        return result

    def check_borrow_status(self, id):
        statement = f"SELECT returned FROM borrows WHERE id = {id}"
        result = self._db.execute_read_query(statement)
        return result

    def update_book_status(self, id, status):
        statement = f"UPDATE books SET status='{status}' WHERE id={id};"
        self._db.execute_query(statement)

    def get_books_statistics_status(self):
        statement = f"SELECT status, COUNT(*) FROM books GROUP BY status;"
        result = self._db.execute_read_query(statement)
        return result

    def get_books_statistics_popularity(self):
        statement = f"""
                    SELECT b.title, COUNT(*) as popularity FROM borrows br INNER JOIN books b ON 
                    br.book_id = b.id GROUP BY b.title ORDER BY popularity DESC LIMIT 5;
                    """
        result = self._db.execute_read_query(statement)
        return result

    def get_readers_statistics_sex(self):
        statement = f"SELECT sex, COUNT(*) FROM readers GROUP BY sex;"
        result = self._db.execute_read_query(statement)
        return result

    def get_readers_statistics_popularity(self):
        statement = f"""
                    SELECT r.name ||' '|| r.surname as person, COUNT(*) as popularity FROM borrows br INNER JOIN
                    readers r ON br.reader_id = r.id GROUP BY person ORDER BY popularity DESC LIMIT 5;
                    """
        result = self._db.execute_read_query(statement)
        return result
