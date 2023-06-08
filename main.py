import tkinter as tik
import tkinter as tk
import psycopg2
from tkinter import messagebox, ttk

# Параметры базы данных
host = 'localhost'
port = '5432'
database = 'Games'
user = 'postgres'
password = 'Zasada0902_2000'


# Настройка первичной формы
class Games(tik.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.title("Ввод данных об игре")
        self.parent = parent
        self.geometry("300x190")
        self.configure(bg="grey")

        self.game_label = tik.Label(self, text="Название:")
        self.game_label.grid(row=0, column=0)
        self.game_entry = tik.Entry(self)
        self.game_entry.grid(row=0, column=1)

        self.status_list = ["Пройдено", "Брошено"]
        self.status_label = tik.Label(self, text="Статус:")
        self.status_label.grid(row=1, column=0)
        self.status_combobox = ttk.Combobox(self, values=self.status_list, state="readonly")
        self.status_combobox.grid(row=1, column=1)

        self.rate_label = tik.Label(self, text="Оценка(от 1 до 10):")
        self.rate_label.grid(row=2, column=0)
        self.rate_combobox = ttk.Combobox(self, values=list(range(1, 11)), state="readonly")
        self.rate_combobox.grid(row=2, column=1)

        self.genre_list = ["Action", "MMORPG", "MUD", "Аркада", "Визуальный роман", "Головоломки", "Интерактивное кино",
                           "Казуальные игры", "Квест", "Менеджеры", "Платформер", "Ролевые игры", "Симулятор",
                           "Стратегии", "Сюжетные развлечения", "Тактические игры", "Файтинг", "Хоррор", "Шутер"]
        self.genre_label = tik.Label(self, text="Жанр:")
        self.genre_label.grid(row=3, column=0)
        self.genre_combobox = ttk.Combobox(self, values=self.genre_list, state="readonly")
        self.genre_combobox.grid(row=3, column=1)

        self.platform_list = ["Android", "IOS", "Linux", "Nintendo", "PlayStation", "Windows", "Xbox"]
        self.platform_label = tik.Label(self, text="Тип:")
        self.platform_label.grid(row=4, column=0)
        self.platform_combobox = ttk.Combobox(self, values=self.platform_list, state="readonly")
        self.platform_combobox.grid(row=4, column=1)

        self.insert_btn = tik.Button(self, text="Внести игру в базу",
                                     command=self.insert_data)

        self.insert_btn.grid(row=5, column=1, columnspan=2)

        self.back_btn = tik.Button(self, text="Назад", command=self.get_back)
        self.back_btn.grid(row=6, column=1, columnspan=2)

    def insert_data(self):
        conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
        cur = conn.cursor()
        rating = int(self.rate_combobox.get())

        data = (
            self.game_entry.get(), self.status_combobox.get(), rating, self.genre_combobox.get(),
            self.platform_combobox.get()
        )
        cur.execute("INSERT INTO GG (title, status, rating, genre, platform) VALUES (%s, %s, %s, %s, %s)", data)
        conn.commit()
        messagebox.showinfo("Успех", "Игры успешно добавлены в таблицу")

        cur.close()
        conn.close()

        self.destroy()
        self.parent.deiconify()

    def get_back(self):
        self.destroy()
        self.parent.deiconify()


class ViewData(tik.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.title("Просмотр данных")
        self.configure(bg="orange")
        self.parent = parent

        self.back_btn = tik.Button(self, text="Назад", command=self.get_back, width=10, height=2)
        self.back_btn.pack()

        self.data_frame = tik.Frame(self)
        self.data_frame.pack()

        self.column_labels = ['Название игры', 'Статус', 'Оценка', 'Жанр', 'Платформа']

        self.read_data()

    def get_back(self):
        self.destroy()
        self.parent.deiconify()

    # Фуникция чтения таблицы бд
    def read_data(self):
        self.title("Данные о пройденых играх")
        self.geometry("700x500")
        conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)

        cur = conn.cursor()
        cur.execute("SELECT * FROM GG")
        results = cur.fetchall()

        # Отчистка предыдущей попытки ввода данных
        for widget in self.data_frame.grid_slaves():
            widget.destroy()

        # Описание колонок
        for col, label_text in enumerate(self.column_labels):
            label = tik.Label(self.data_frame, text=label_text, font='bold')
            label.grid(row=0, column=col)

        # Отображение наших данных
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                if col == 2:  # Оценка пройденых игр
                    value = str(value)  # Изменение типа для отображение в базе
                label = tik.Label(self.data_frame, text=value)
                label.grid(row=row + 1, column=col)

            delete_btn = tik.Button(self.data_frame, text="Удалить", command=lambda row=row: self.delete_data(row))
            delete_btn.grid(row=row + 1, column=7)

        cur.close()
        conn.close()

    # Функция удаления
    def delete_data(self, row):
        conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
        cur = conn.cursor()

        cur.execute("SELECT * FROM GG")
        results = cur.fetchall()

        # Получение идентификатора игр для удаления
        delete_title = results[row][0]

        cur.execute("DELETE FROM GG WHERE title = %s", (delete_title,))
        conn.commit()

        cur.close()
        conn.close()

        # Повторный просмотр базы для графического интерфейсика
        self.read_data()


class Edit_data(tik.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title("Изменение записи")
        self.geometry("300x180")
        self.configure(bg="violet")
        self.parent = parent

        self.game_label = tik.Label(self, text="Название:")
        self.game_label.grid(row=0, column=0)
        self.game_entry = tik.Entry(self)
        self.game_entry.grid(row=0, column=1)

        self.status_list = ["Пройдено", "Брошено"]
        self.status_label = tik.Label(self, text="Статус:")
        self.status_label.grid(row=1, column=0)
        self.status_combobox = ttk.Combobox(self, values=self.status_list, state="readonly")
        self.status_combobox.grid(row=1, column=1)

        self.rate_label = tik.Label(self, text="Оценка игры от 1 до 10:")
        self.rate_label.grid(row=2, column=0)
        self.rate_combobox = ttk.Combobox(self, values=list(range(1, 11)), state="readonly")
        self.rate_combobox.grid(row=2, column=1)

        self.genre_list = ["Action", "MMORPG", "MUD", "Аркада", "Визуальный роман", "Головоломки", "Интерактивное кино",
                           "Казуальные игры", "Квест", "Менеджеры", "Платформер", "Ролевые игры", "Симулятор",
                           "Стратегии", "Сюжетные развлечения", "Тактические игры", "Файтинг", "Хоррор", "Шутер"]
        self.genre_label = tik.Label(self, text="Жанр:")
        self.genre_label.grid(row=3, column=0)
        self.genre_combobox = ttk.Combobox(self, values=self.genre_list, state="readonly")
        self.genre_combobox.grid(row=3, column=1)

        self.platform_list = ["Android", "IOS", "Linux", "Nintendo", "PlayStation", "Windows", "Xbox"]
        self.platform_label = tik.Label(self, text="Тип:")
        self.platform_label.grid(row=4, column=0)
        self.platform_combobox = ttk.Combobox(self, values=self.platform_list, state="readonly")
        self.platform_combobox.grid(row=4, column=1)

        self.search_button = tik.Button(self, text="Поиск по названию", command=self.search_by_title)
        self.search_button.grid(row=5, column=0, columnspan=2)

        self.update_button = tik.Button(self, text="Обновить данные", command=self.update_data)
        self.update_button.grid(row=6, column=0, columnspan=2)

        self.back_btn = tik.Button(self, text="Назад", command=self.get_back)
        self.back_btn.grid(row=7, column=0, columnspan=2)

        self.conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
        self.cursor = self.conn.cursor()

    def get_back(self):
        self.destroy()
        self.parent.deiconify()

    def fetch_data(self):
        self.cursor.execute("SELECT title, status, rating, genre, "
                            "platform FROM GG")
        result = self.cursor.fetchone()

        if result:
            self.game_entry.insert(0, result[0])
            self.status_combobox.set(result[1])
            self.rate_combobox.set(result[2])
            self.genre_combobox.insert(0, result[3])
            self.platform_combobox.insert(0, result[4])

    def search_by_title(self):
        title = self.game_entry.get()
        self.cursor.execute("SELECT title, status, rating, genre, platform"
                            " FROM GG WHERE title=%s", (title,))
        result = self.cursor.fetchone()

        if result:
            self.status_combobox.set(result[1])

            self.rate_combobox.set(result[2])

            self.genre_combobox.set(result[3])

            self.platform_combobox.set(result[4])

            messagebox.showinfo("Результат поиска", "Запись найдена!")
        else:
            messagebox.showinfo("Результат поиска", "Запись не найдена.")

    def update_data(self):
        title = self.game_entry.get()
        status = self.status_combobox.get()
        rating = self.rate_combobox.get()
        genre = self.genre_combobox.get()
        platform = self.platform_combobox.get()

        self.cursor.execute("UPDATE GG SET title=%s, status=%s, rating=%s, genre=%s, platform=%s WHERE title=%s",
                            (title, status, rating, genre, platform, title))
        self.conn.commit()

        messagebox.showinfo("Обновлено", "Данные успешно обновлены!")


# Создание главной формы для всей программы
class MainForm(tik.Tk):
    def __init__(self):
        super().__init__()

        self.title("Главный экран")
        self.geometry("300x100")
        self.configure(bg="blue")

        self.input_btn = tik.Button(self, text="Внести данные об игре", command=self.open_input_form)
        self.input_btn.pack()

        self.view_btn = tik.Button(self, text="Просмотр данных", command=self.open_view_form)
        self.view_btn.pack()

        self.edit_btn = tik.Button(self, text="Изменить запись", command=self.open_editer_form)
        self.edit_btn.pack()

    def open_view_form(self):
        self.withdraw()
        view_form = ViewData(self)
        view_form.protocol("WM_DELETE_WINDOW", self.on_close_view_form)

    def open_input_form(self):
        self.withdraw()
        input_form = Games(self)
        input_form.protocol("WM_DELETE_WINDOW", self.on_close_input_form)

    def open_editer_form(self):
        self.withdraw()
        edit_form = Edit_data(self)
        edit_form.protocol("WM_DELETE_WINDOW", self.on_close_edit_form)

    def on_close_input_form(self):
        self.withdraw()
        self.deiconify()

    def on_close_view_form(self):
        self.withdraw()
        self.deiconify()

    def on_close_edit_form(self):
        self.withdraw()
        self.deiconify()


if __name__ == "__main__":
    main_form = MainForm()
    main_form.mainloop()
