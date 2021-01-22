from model import Model
from view import View
from datetime import date, timedelta


class Controller:
    def __init__(self):
        self._view = View(self)
        self._model = Model()

    def _main(self):
        self._view.main()

    def change_to_books_panel(self, action, id_number=''):
        if action == 'Add':
            self._view.clear_window()
            self._view.show_books_panel(action=action)
        else:  # in case of action=edit and action=delete there is need to check if provided book id is valid
            if id_number.isnumeric():
                book = self._model.get_book(id_number)
                if book:  # means record exists in db
                    self._view.clear_window()
                    self._view.show_books_panel(action=action, id_number=id_number, title=book[0][1],
                                                authors=book[0][2],
                                                year=book[0][3],
                                                status=book[0][4], isbn=book[0][5])
                else:  # id do not exists in database
                    self._view.show_error_msg('Invalid ID', 'Please provide valid ID')
            else:
                self._view.show_error_msg('Invalid ID', 'Please provide valid ID')

    def change_to_readers_panel(self, action, id_number=''):
        if action == 'Add':
            self._view.clear_window()
            self._view.show_readers_panel(action=action)
        else:  # in case of action=edit and action=delete there is need to check if provided reader id is valid
            if id_number.isnumeric():
                reader = self._model.get_reader(id_number)
                if reader:  # means record exists in db
                    self._view.clear_window()
                    self._view.show_readers_panel(action=action, id_number=id_number, name=reader[0][1],
                                                  surname=reader[0][2],
                                                  birth=reader[0][3], sex=reader[0][4], nat_id=reader[0][5])
                else:  # id do not exists in database
                    self._view.show_error_msg('Invalid ID', 'Please provide valid ID')
            else:
                self._view.show_error_msg('Invalid ID', 'Please provide valid ID')

    def change_to_books_view(self, search=''):
        self._view.clear_window()
        books = self._model.get_books(search)
        self._view.show_books_view(books)

    def change_to_readers_view(self, search=''):
        self._view.clear_window()
        reader = self._model.get_readers(search)
        self._view.show_readers_view(reader)

    def change_to_borrows_view(self, search=''):
        self._view.clear_window()
        borrows = self._model.get_borrows(search)
        self._view.show_borrows_view(borrows)

    def change_to_borrows_panel(self, book_id='', reader_id='', act_book='', act_reader=''):
        book, reader = '', ''
        if book_id:
            book = self._model.get_book(book_id)
            if not book:
                self._view.show_error_msg('Invalid ID', 'Please provide valid ID')
                return
        if reader_id:
            reader = self._model.get_reader(reader_id)
            if not reader:
                self._view.show_error_msg('Invalid ID', 'Please provide valid ID')
                return
        self._view.clear_window()
        if act_book:  # when book is already selected
            self._view.show_borrowing_panel(act_book, reader)
        elif act_reader:  # when reader is already selected
            self._view.show_borrowing_panel(book, act_reader)
        else:  # for page without selected book and reader
            self._view.show_borrowing_panel(book, reader)

    def button_canel(self):
        self._view.clear_window()
        self._view.show_welcome_page()

    # one function for different actions
    def perform_book_action(self, action, id_number, title, author, year, status, isbn):
        if title == '' or author == '' or year == '' or status == '' or isbn == '':  # all fields are required
            self._view.show_error_msg('Missing data', 'Please fill all fields')
        elif (not year.isnumeric()) or (not isbn.isnumeric()):  # year and isbn have to be numeric
            self._view.show_error_msg('Invalid data type', 'Year and ISBN need to be numeric')
        elif len(isbn) != 13:  # ISBN is 13 digit number
            self._view.show_error_msg('Invalid ISBN number', 'Please correct ISBN number')
        else:
            if action == 'Add':
                if self._view.show_yesno_msg():  # returns True if 'Yes' was pressed
                    self._model.insert_into_books(title, author, int(year), status, int(isbn))
                else:
                    return  # do not change view in case confirmation is not received
            elif action == 'Edit':
                if self._view.show_yesno_msg():  # returns True if 'Yes' was pressed
                    self._model.update_book(id_number, title, author, int(year), status, int(isbn))
                else:
                    return  # do not change view in case confirmation is not received
            elif action == 'Delete':
                if self._view.show_yesno_msg():  # returns True if 'Yes' was pressed
                    self._model.delete_book(id_number)
                else:
                    return  # do not change view in case confirmation is not received
            self._view.clear_window()
            self._view.show_welcome_page()

    def perform_reader_action(self, action, id_number, name, surname, birth, sex, nat_id):
        if name == '' or surname == '' or birth == '' or sex == '' or nat_id == '':  # all fields are required
            self._view.show_error_msg('Missing data', 'Please fill all fields')
        elif not nat_id.isnumeric():  # nat_id has to be numeric
            self._view.show_error_msg('Invalid data type', 'National ID need to be numeric')
        elif len(nat_id) != 11:  # nat_id is 11 digit number
            self._view.show_error_msg('Invalid National ID', 'Please correct National ID number')
        else:
            if action == 'Add':
                if self._view.show_yesno_msg():  # returns True if 'Yes' was pressed
                    self._model.insert_into_readers(name, surname, birth, sex, nat_id)
                else:
                    return  # do not change view in case confirmation is not received
            elif action == 'Edit':
                if self._view.show_yesno_msg():  # returns True if 'Yes' was pressed
                    self._model.update_reader(id_number, name, surname, birth, sex, nat_id)
                else:
                    return  # do not change view in case confirmation is not received
            elif action == 'Delete':
                if self._view.show_yesno_msg():  # returns True if 'Yes' was pressed
                    self._model.delete_reader(id_number)
                else:
                    return  # do not change view in case confirmation is not received
            self._view.clear_window()
            self._view.show_welcome_page()

    def borrow_book(self, book_id, reader_id):
        if self._view.show_yesno_msg():  # to confirm
            status = self._model.check_book_status(book_id)
            if status[0][0] == 'Active':  # Book can be borrowed
                self._model.update_book_status(book_id, 'Borrowed')
                borrow_date = date.today()
                return_date = borrow_date + timedelta(days=30)  # 30 days to return book
                self._model.insert_into_borrows(book_id, reader_id, str(borrow_date), str(return_date))
                self._view.clear_window()
                self._view.show_welcome_page()
            else:  # Book can not be borrowed
                self._view.show_error_msg('Error', 'This book is already borrowed')

    def return_book(self, borrow_id, book_id):
        if borrow_id:  # to avoid situation where no record was selected
            borrow_status = self._model.check_borrow_status(borrow_id)[0][0]
            if borrow_status is None:
                returned = date.today()
                self._model.update_book_status(book_id, 'Active')  # set book active again
                self._model.update_borrows_returned(borrow_id, returned)  # edit borrow record
                self.change_to_borrows_view('')
            else:
                self._view.show_error_msg('Error', 'This book was already returned')

    def prolong_book(self, borrow_id):
        if borrow_id:  # to avoid situation where no record was selected
            borrow_status = self._model.check_borrow_status(borrow_id)[0][0]
            if borrow_status is None:
                prolonged_date = date.today() + timedelta(days=30)  # 30 days from today
                self._model.update_borrows_return_date(borrow_id, prolonged_date)  # edit borrow record
                self.change_to_borrows_view('')
            else:
                self._view.show_error_msg('Error', 'This book was already returned')

    def change_to_books_statistics(self):
        self._view.clear_window()
        status = self._model.get_books_statistics_status()
        popularity = self._model.get_books_statistics_popularity()
        print(popularity)
        status_series = []
        status_num_series = []
        title_series = []
        title_num_series = []
        for record in status:
            status_series.append(record[0])
            status_num_series.append(record[1])
        for record in popularity:
            title_series.append(record[0])
            title_num_series.append(record[1])
        self._view.show_books_statistics(status_series, status_num_series, title_series, title_num_series)

    def change_to_readers_statistics(self):
        self._view.clear_window()
        s = self._model.get_readers_statistics_sex()
        popularity = self._model.get_readers_statistics_popularity()
        print(popularity)
        s_series = []
        s_num_series = []
        reader_series = []
        reader_num_series = []
        for record in s:
            s_series.append(record[0])
            s_num_series.append(record[1])
        for record in popularity:
            reader_series.append(record[0])
            reader_num_series.append(record[1])
        self._view.show_readers_statistics(s_series, s_num_series, reader_series, reader_num_series)

    def show_id_window(self, action, type):
        self._view.clear_window()
        self._view.show_id_request(action=action, type=type)


controller = Controller()
controller._main()
