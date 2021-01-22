from tkinter import ttk
import tkinter.font as font
import tkinter as tk
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class View:
    def __init__(self, controller):
        self._controller = controller
        self._root = tk.Tk()
        self._root.minsize(640, 480)
        self._imgbook = tk.PhotoImage(file="book.png")
        self._imgreader = tk.PhotoImage(file="read.png")
        self._root.iconphoto(False, self._imgbook)
        self._root.title("Your Library")
        self._create_menu()
        self.show_welcome_page()
        self._root.columnconfigure([0, 1], weight=1)  # no more than 2 columns required, if less span function available
        self._root.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)  # no more than 6 rows required
        self._lblFont = font.Font(family='Verdana', size=10)
        self._buttonFont = font.Font(family='Helvetica', size=10)

    def _create_menu(self):
        menubar = tk.Menu(self._root)

        books_menu = tk.Menu(menubar, tearoff=0)
        books_menu.add_command(label='Add', command=lambda: self._controller.change_to_books_panel('Add'))
        books_menu.add_command(label='Edit', command=lambda: self._controller.show_id_window('Edit', 'Book'))
        books_menu.add_command(label='Delete', command=lambda: self._controller.show_id_window('Delete', 'Book'))
        books_menu.add_command(label='View', command=lambda: self._controller.change_to_books_view())

        readers_menu = tk.Menu(menubar, tearoff=0)
        readers_menu.add_command(label='Add', command=lambda: self._controller.change_to_readers_panel('Add'))
        readers_menu.add_command(label='Edit', command=lambda: self._controller.show_id_window('Edit', 'Reader'))
        readers_menu.add_command(label='Delete', command=lambda: self._controller.show_id_window('Delete', 'Reader'))
        readers_menu.add_command(label='View', command=lambda: self._controller.change_to_readers_view())

        borrowings_menu = tk.Menu(menubar, tearoff=0)
        borrowings_menu.add_command(label='New', command=self._controller.change_to_borrows_panel)
        borrowings_menu.add_command(label='Prolong/Return', command=self._controller.change_to_borrows_view)

        statistics_menu = tk.Menu(menubar, tearoff=0)
        statistics_menu.add_command(label='Books', command=self._controller.change_to_books_statistics)
        statistics_menu.add_command(label='Readers', command=self._controller.change_to_readers_statistics)

        menubar.add_cascade(label='Books', menu=books_menu)
        menubar.add_cascade(label='Readers', menu=readers_menu)
        menubar.add_cascade(label='Borrowings', menu=borrowings_menu)
        menubar.add_cascade(label='Statistics', menu=statistics_menu)

        self._root.config(menu=menubar)

    def show_welcome_page(self):
        lbl_welcome = tk.Label(self._root, text='Welcome to library system', bg='grey', font='Helvetica 32 bold italic')
        lbl_book = tk.Label(self._root, bg='grey', image=self._imgbook)

        lbl_welcome.grid(row=0, column=0, rowspan=3, columnspan=2, sticky='nsew')
        lbl_book.grid(row=3, column=0, rowspan=3, columnspan=2, sticky='nsew')

    def show_books_view(self, books):
        lbl_search = tk.Label(self._root, text='Search by Title:', font=self._lblFont)
        ent_search = tk.Entry(self._root, width=30)
        btn_search = tk.Button(self._root, text='Search', bg='grey84', height=2, width=8, font=self._buttonFont,
                               command=lambda: self._controller.change_to_books_view(ent_search.get()))
        treev = ttk.Treeview(self._root, selectmode='browse')
        verscrlbar = ttk.Scrollbar(self._root, orient="vertical", command=treev.yview)

        lbl_search.grid(row=0, column=0, columnspan=2, sticky='ew')
        ent_search.grid(row=1, column=0, columnspan=2)
        btn_search.grid(row=2, column=0, columnspan=2)
        treev.grid(row=3, column=0, rowspan=3, padx=(10, 10), pady=(5, 5), sticky='nsew')
        verscrlbar.grid(row=3, column=1, rowspan=3, sticky='nse')

        treev.configure(xscrollcommand=verscrlbar.set)
        treev['columns'] = ('1', '2', '3', '4', '5', '6')
        treev['show'] = 'headings'

        treev.column("1", width=100, anchor='c')
        treev.column("2", width=100, anchor='c')
        treev.column("3", width=100, anchor='c')
        treev.column("4", width=100, anchor='c')
        treev.column("5", width=100, anchor='c')
        treev.column("6", width=100, anchor='c')

        treev.heading("1", text="ID")
        treev.heading("2", text="Title")
        treev.heading("3", text="Author")
        treev.heading("4", text="Year")
        treev.heading("5", text="Status")
        treev.heading("6", text="ISBN")

        for book in books:
            treev.insert("", 'end', values=book)

    def show_readers_view(self, readers):
        lbl_search = tk.Label(self._root, text='Search by Surname:', font=self._lblFont)
        ent_search = tk.Entry(self._root, width=30)
        btn_search = tk.Button(self._root, text='Search', bg='grey84', height=2, width=8, font=self._buttonFont,
                               command=lambda: self._controller.change_to_readers_view(ent_search.get()))
        treev = ttk.Treeview(self._root, selectmode='browse')
        verscrlbar = ttk.Scrollbar(self._root, orient="vertical", command=treev.yview)

        lbl_search.grid(row=0, column=0, columnspan=2, sticky='ew')
        ent_search.grid(row=1, column=0, columnspan=2)
        btn_search.grid(row=2, column=0, columnspan=2)
        treev.grid(row=3, column=0, rowspan=3, padx=(10, 10), pady=(5, 5), sticky='nsew')
        verscrlbar.grid(row=3, column=1, rowspan=3, sticky='nse')

        treev.configure(xscrollcommand=verscrlbar.set)
        treev['columns'] = ('1', '2', '3', '4', '5', '6')
        treev['show'] = 'headings'

        treev.column("1", width=100, anchor='c')
        treev.column("2", width=100, anchor='c')
        treev.column("3", width=100, anchor='c')
        treev.column("4", width=100, anchor='c')
        treev.column("5", width=100, anchor='c')
        treev.column("6", width=100, anchor='c')

        treev.heading("1", text="ID")
        treev.heading("2", text="Name")
        treev.heading("3", text="Surname")
        treev.heading("4", text="Date of Birth")
        treev.heading("5", text="Sex")
        treev.heading("6", text="National ID")

        for reader in readers:
            treev.insert("", 'end', values=reader)

    def show_borrows_view(self, borrows):
        treev = ttk.Treeview(self._root, selectmode='browse')

        def get_item(num):
            try:
                item = treev.item(treev.focus())['values'][num]
            except IndexError:
                item = ''
            return item

        ent_search = tk.Entry(self._root, width=35, fg='grey')
        btn_search = tk.Button(self._root, text='Search', bg='grey84', height=2, width=8, font=self._buttonFont,
                               command=lambda: self._controller.change_to_borrows_view(ent_search.get()))
        ent_search.insert(tk.END, 'Search by title or reader')
        btn_prolong = tk.Button(self._root, text='Prolong', bg='grey84', height=2, width=10, font=self._buttonFont,
                                command=lambda: self._controller.prolong_book(get_item(0)))
        btn_return = tk.Button(self._root, text='Return', bg='grey84', height=2, width=10, font=self._buttonFont,
                               command=lambda: self._controller.return_book(get_item(0),
                                                                            get_item(1)))
        btn_cancel = tk.Button(self._root, text='Cancel', bg='grey84', height=2, width=10, font=self._buttonFont,
                               command=self._controller.button_canel)  # go back to welcome page

        ent_search.grid(row=0, column=0)
        btn_search.grid(row=0, column=1, sticky='w')
        treev.grid(row=1, column=0, rowspan=3, columnspan=2, padx=(10, 10), pady=(5, 5), sticky='nsew')
        btn_prolong.grid(row=4, column=0)
        btn_return.grid(row=4, column=1, sticky='w')
        btn_cancel.grid(row=5, column=0, columnspan=2)

        treev['columns'] = ('1', '2', '3', '4', '5', '6', '7', '8')
        treev['show'] = 'headings'

        treev.column("1", width=50, anchor='c')
        treev.column("2", width=50, anchor='c')
        treev.column("3", width=90, anchor='c')
        treev.column("4", width=90, anchor='c')
        treev.column("5", width=90, anchor='c')
        treev.column("6", width=90, anchor='c')
        treev.column("7", width=90, anchor='c')
        treev.column("8", width=90, anchor='c')

        treev.heading("1", text="ID")
        treev.heading("2", text='Book ID')
        treev.heading("3", text="Title")
        treev.heading("4", text="ISBN")
        treev.heading("5", text="Reader")
        treev.heading("6", text="Borrow Date")
        treev.heading("7", text="Return Date")
        treev.heading("8", text="Returned")

        for borrow in borrows:
            treev.insert("", 'end', values=borrow)

    def show_books_panel(self, action='', id_number='', title='', authors='', year='', status='Active', isbn=''):
        cmd = None
        stat = 'normal'
        if action == '':
            return  # show nothing in case type of action is not valid
        elif action == 'Add':
            cmd = lambda: self._controller.perform_book_action('Add', id_number, ent_title.get(), ent_authors.get(),
                                                               ent_year.get(),
                                                               ent_status.get(), ent_isbn.get())
        elif action == 'Edit':
            cmd = lambda: self._controller.perform_book_action('Edit', id_number, ent_title.get(), ent_authors.get(),
                                                               ent_year.get(),
                                                               ent_status.get(), ent_isbn.get())
        elif action == 'Delete':
            cmd = lambda: self._controller.perform_book_action('Delete', id_number, ent_title.get(), ent_authors.get(),
                                                               ent_year.get(), ent_status.get(), ent_isbn.get())
            stat = 'disabled'  # There is no need to modify record, which will be deleted
        lbl_title = tk.Label(self._root, text='Title:', font=self._lblFont)
        lbl_authors = tk.Label(self._root, text='Authors:', font=self._lblFont)
        lbl_year = tk.Label(self._root, text='Year of publishment:', font=self._lblFont)
        lbl_status = tk.Label(self._root, text='Status:', font=self._lblFont)
        lbl_isbn = tk.Label(self._root, text='ISBN:', font=self._lblFont)

        ent_title = tk.Entry(self._root, width=35)
        ent_authors = tk.Entry(self._root, width=35)
        ent_year = tk.Entry(self._root, width=35)
        ent_status = tk.Entry(self._root, width=35)
        ent_isbn = tk.Entry(self._root, width=35)

        ent_title.insert(tk.END, title)
        ent_authors.insert(tk.END, authors)
        ent_year.insert(tk.END, year)
        ent_status.insert(tk.END, status)
        ent_isbn.insert(tk.END, isbn)

        ent_title.config(state=stat)
        ent_authors.config(state=stat)
        ent_year.config(state=stat)
        ent_status.config(state='disabled')
        ent_isbn.config(state=stat)

        btn_cancel = tk.Button(self._root, text='Cancel', bg='grey84', height=2, width=10, font=self._buttonFont,
                               command=self._controller.button_canel)  # go back to welcome page
        btn_ok = tk.Button(self._root, text=action, bg='grey84', height=2, width=10, font=self._buttonFont,
                           command=cmd)

        lbl_title.grid(row=0, column=0)
        lbl_authors.grid(row=1, column=0)
        lbl_year.grid(row=2, column=0)
        lbl_status.grid(row=3, column=0)
        lbl_isbn.grid(row=4, column=0)

        ent_title.grid(row=0, column=1)
        ent_authors.grid(row=1, column=1)
        ent_year.grid(row=2, column=1)
        ent_status.grid(row=3, column=1)
        ent_isbn.grid(row=4, column=1)

        btn_cancel.grid(row=5, column=0)
        btn_ok.grid(row=5, column=1)

    def show_readers_panel(self, action='', id_number='', name='', surname='', birth='', sex='', nat_id=''):
        cmd = None
        status = 'normal'
        if action == '':
            return  # show nothing in case type of action is not valid
        elif action == 'Add':
            cmd = lambda: self._controller.perform_reader_action('Add', id_number, ent_name.get(), ent_surname.get(),
                                                                 ent_birth.get(),
                                                                 ent_sex.get(), ent_nat_id.get())
        elif action == 'Edit':
            cmd = lambda: self._controller.perform_reader_action('Edit', id_number, ent_name.get(), ent_surname.get(),
                                                                 ent_birth.get(),
                                                                 ent_sex.get(), ent_nat_id.get())
        elif action == 'Delete':
            cmd = lambda: self._controller.perform_reader_action('Delete', id_number, ent_name.get(), ent_surname.get(),
                                                                 ent_birth.get(), ent_sex.get(), ent_nat_id.get())
            status = 'disabled'  # There is no need to modify record, which will be deleted
        lbl_name = tk.Label(self._root, text='Name:', font=self._lblFont)
        lbl_surname = tk.Label(self._root, text='Surname:', font=self._lblFont)
        lbl_birth = tk.Label(self._root, text='Date of birth:', font=self._lblFont)
        lbl_sex = tk.Label(self._root, text='Sex:', font=self._lblFont)
        lbl_nat_id = tk.Label(self._root, text='National ID:', font=self._lblFont)

        ent_name = tk.Entry(self._root, width=35)
        ent_surname = tk.Entry(self._root, width=35)
        ent_birth = tk.Entry(self._root, width=35)
        ent_sex = tk.Entry(self._root, width=35)
        ent_nat_id = tk.Entry(self._root, width=35)

        ent_name.insert(tk.END, name)
        ent_surname.insert(tk.END, surname)
        ent_birth.insert(tk.END, birth)
        ent_sex.insert(tk.END, sex)
        ent_nat_id.insert(tk.END, nat_id)

        ent_name.config(state=status)
        ent_surname.config(state=status)
        ent_birth.config(state=status)
        ent_sex.config(state=status)
        ent_nat_id.config(state=status)

        btn_cancel = tk.Button(self._root, text='Cancel', bg='grey84', height=2, width=10, font=self._buttonFont,
                               command=self._controller.button_canel)  # go back to welcome page
        btn_ok = tk.Button(self._root, text=action, bg='grey84', height=2, width=10, font=self._buttonFont,
                           command=cmd)

        lbl_name.grid(row=0, column=0)
        lbl_surname.grid(row=1, column=0)
        lbl_birth.grid(row=2, column=0)
        lbl_sex.grid(row=3, column=0)
        lbl_nat_id.grid(row=4, column=0)

        ent_name.grid(row=0, column=1)
        ent_surname.grid(row=1, column=1)
        ent_birth.grid(row=2, column=1)
        ent_sex.grid(row=3, column=1)
        ent_nat_id.grid(row=4, column=1)

        btn_cancel.grid(row=5, column=0)
        btn_ok.grid(row=5, column=1)

    def show_borrowing_panel(self, book, reader):
        lbl_reader = tk.Label(self._root, image=self._imgreader)
        ent_book_id = tk.Entry(self._root, width=30, fg='grey')
        ent_reader_id = tk.Entry(self._root, width=30, fg='grey')
        btn_book_search = tk.Button(self._root, text='Search for Book', bg='grey80', height=2, width=15,
                                    font=self._buttonFont,
                                    command=lambda: self._controller.change_to_borrows_panel(
                                        book_id=ent_book_id.get(), act_reader=reader))
        btn_reader_search = tk.Button(self._root, text='Search for Reader', bg='grey80', height=2, width=15,
                                      font=self._buttonFont,
                                      command=lambda: self._controller.change_to_borrows_panel(
                                          reader_id=ent_reader_id.get(), act_book=book))
        str_book, str_reader = '', ''
        if book:
            str_book = f'Title: {book[0][1]}, Authors: {book[0][2]}, ISBN: {book[0][5]}'
        if reader:
            str_reader = f'Name: {reader[0][1]} {reader[0][2]}, Born: {reader[0][3]}, National ID: {reader[0][5]}'
        lblresult = font.Font(family='Arial', size=11)
        lbl_book_result = tk.Label(self._root, bg='seashell2', height=2, text=str_book, font=lblresult,
                                   relief=tk.SUNKEN)
        lbl_reader_result = tk.Label(self._root, bg='seashell2', height=2, text=str_reader, font=lblresult,
                                     relief=tk.SUNKEN)

        if book:
            ent_book_id.insert(tk.END, book[0][0])
        else:
            ent_book_id.insert(tk.END, 'Book ID')
        if reader:
            ent_reader_id.insert(tk.END, reader[0][0])
        else:
            ent_reader_id.insert(tk.END, 'Reader ID')

        lbl_reader.grid(row=0, column=0, columnspan=2)
        ent_book_id.grid(row=1, column=0)
        btn_book_search.grid(row=1, column=1)
        lbl_book_result.grid(row=2, column=0, columnspan=2, sticky='ew', padx=(15, 15), pady=(5, 5))
        ent_reader_id.grid(row=3, column=0)
        btn_reader_search.grid(row=3, column=1)
        lbl_reader_result.grid(row=4, column=0, columnspan=2, sticky='ew', padx=(15, 15), pady=(5, 5))

        btn_cancel = tk.Button(self._root, text='Cancel', bg='grey84', height=2, width=10, font=self._buttonFont,
                               command=self._controller.button_canel)  # go back to welcome page
        btn_borrow = tk.Button(self._root, text='Borrow', bg='grey84', height=2, width=10, font=self._buttonFont,
                               command=lambda: self._controller.borrow_book(book[0][0], reader[0][0]))

        btn_cancel.grid(row=5, column=0)
        btn_borrow.grid(row=5, column=1)

    def show_id_request(self, action='', type=''):
        cmd = None
        if action == '':
            return  # show nothing in case type of action is not valid
        elif action == 'Edit' and type == 'Book':
            cmd = lambda: self._controller.change_to_books_panel('Edit', id_number=(ent_id.get()))
        elif action == 'Delete' and type == 'Book':
            cmd = lambda: self._controller.change_to_books_panel('Delete', id_number=(ent_id.get()))
        elif action == 'Edit' and type == 'Reader':
            cmd = lambda: self._controller.change_to_readers_panel('Edit', id_number=(ent_id.get()))
        elif action == 'Delete' and type == 'Reader':
            cmd = lambda: self._controller.change_to_readers_panel('Delete', id_number=(ent_id.get()))
        lbl_id = tk.Label(self._root, text='ID:', font=self._lblFont)
        ent_id = tk.Entry(self._root, width=35)
        btn_cancel = tk.Button(self._root, text='Cancel', bg='grey84', height=2, width=10, font=self._buttonFont,
                               command=self._controller.button_canel)
        btn_proceed = tk.Button(self._root, text='Proceed', bg='grey84', height=2, width=10, font=self._buttonFont,
                                command=cmd)

        lbl_id.grid(row=1, column=0)
        ent_id.grid(row=1, column=1)
        btn_cancel.grid(row=2, column=0)
        btn_proceed.grid(row=2, column=1)

    def show_books_statistics(self, status_series, status_num_series, title_series, title_num_series):
        # Number of books in comparison to actual status of book
        df1 = pd.DataFrame({'Status': status_series, 'Number of Books': status_num_series})
        figure1 = plt.Figure(figsize=(2, 3), dpi=100)
        figure1.subplots_adjust(bottom=0.4)
        ax1 = figure1.add_subplot(111)
        chart = FigureCanvasTkAgg(figure1, self._root)
        chart.get_tk_widget().grid(row=0, column=0, rowspan=6, sticky='nsew')
        df1 = df1[['Status', 'Number of Books']].groupby('Status').sum()
        df1.plot(kind='pie', subplots=True, ax=ax1, legend=None)
        ax1.set_title("Number of books by actual status")

        # Number of borrows by title
        df2 = pd.DataFrame({'Title': title_series, 'Number of Borrows': title_num_series})
        figure2 = plt.Figure(figsize=(2, 3), dpi=100)
        figure2.subplots_adjust(bottom=0.4)
        ax2 = figure2.add_subplot(111)
        chart = FigureCanvasTkAgg(figure2, self._root)
        chart.get_tk_widget().grid(row=0, column=1, rowspan=6, sticky='nsew')
        df2 = df2[['Title', 'Number of Borrows']].groupby('Title').sum()
        df2.plot(kind='bar', ax=ax2, legend=None)
        ax2.set_title("Top 5 titles popularity")

    def show_readers_statistics(self, s_series, s_num_series, reader_series, reader_num_series):
        # Number of readers in comparison to Sex
        df1 = pd.DataFrame({'Sex': s_series, 'Number of Readers': s_num_series})
        figure1 = plt.Figure(figsize=(2, 3), dpi=100)
        figure1.subplots_adjust(bottom=0.4)
        ax1 = figure1.add_subplot(111)
        chart = FigureCanvasTkAgg(figure1, self._root)
        chart.get_tk_widget().grid(row=0, column=0, rowspan=6, sticky='nsew')
        df1 = df1[['Sex', 'Number of Readers']].groupby('Sex').sum()
        df1.plot(kind='pie', subplots=True, ax=ax1, legend=None)
        ax1.set_title("Number of Readers by Sex")

        # Number of borrows per reader
        df2 = pd.DataFrame({'Reader': reader_series, 'Number of Borrows': reader_num_series})
        figure2 = plt.Figure(figsize=(2, 3), dpi=100)
        figure2.subplots_adjust(bottom=0.4)
        ax2 = figure2.add_subplot(111)
        chart = FigureCanvasTkAgg(figure2, self._root)
        chart.get_tk_widget().grid(row=0, column=1, rowspan=6, sticky='nsew')
        df2 = df2[['Reader', 'Number of Borrows']].groupby('Reader').sum()
        df2.plot(kind='bar', ax=ax2, legend=None)
        ax2.set_title("Top 5 Readers")

    def show_error_msg(self, title, text):
        tk.messagebox.showerror(title, text)

    def show_yesno_msg(self):
        return tk.messagebox.askyesno('Confirmation', 'Are you sure?')

    def clear_window(self):
        for widget in self._root.winfo_children():
            if not isinstance(widget, tk.Menu):  # save app menu from destroying
                widget.destroy()

    def main(self):
        self._root.mainloop()
