import tkinter as tk
from tkinter import messagebox, font
from tkcalendar import DateEntry
import sqlite3


def create_db():
    conn = sqlite3.connect("grades.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            grade INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def check_table_structure():
    conn = sqlite3.connect("grades.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(grades);")
    columns = cursor.fetchall()
    for column in columns:
        print(column)
    conn.close()


def add_grade():
    student_name = surname_entry.get().strip()
    subject = subject_entry.get().strip()
    grade = grade_entry.get().strip()
    date = date_entry.get()

    if (
        not student_name
        or not subject
        or not grade.isdigit()
        or not is_valid_date(date)
    ):
        messagebox.showwarning(
            "Ошибка",
            "Пожалуйста, заполните все поля корректно. Дата должна быть в формате дд.мм.гггг.",
        )
        return

    try:
        conn = sqlite3.connect("grades.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO grades (student_name, subject, grade, date) VALUES (?, ?, ?, ?)",
            (student_name, subject, int(grade), date),
        )
        conn.commit()
        conn.close()

        load_grades()
        clear_entries()
        messagebox.showinfo("Успех", "Запись успешно добавлена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось добавить запись: {e}")


def is_valid_date(date_str):
    try:
        day, month, year = map(int, date_str.split("."))
        if 1 <= month <= 12 and 1 <= day <= 31:
            return True
        return False
    except ValueError:
        return False


def delete_grade():
    selected_item = listbox.curselection()
    if selected_item:
        item_id = listbox.get(selected_item)[0]
        conn = sqlite3.connect("grades.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grades WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
        load_grades()
    else:
        messagebox.showwarning("Ошибка", "Выберите запись для удаления.")


def load_grades():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect("grades.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grades")
    for row in cursor.fetchall():
        listbox.insert(tk.END, row)
    conn.close()


def search_grades():
    search_term = search_entry.get().strip()
    listbox.delete(0, tk.END)

    conn = sqlite3.connect("grades.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM grades WHERE student_name LIKE ? OR subject LIKE ?",
        (f"%{search_term}%", f"%{search_term}%"),
    )

    for row in cursor.fetchall():
        listbox.insert(tk.END, row)

    conn.close()


def search_by_date_range():
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()

    if not is_valid_date(start_date) or not is_valid_date(end_date):
        messagebox.showwarning(
            "Ошибка", "Пожалуйста, введите корректные даты в формате дд.мм.гггг."
        )
        return

    listbox.delete(0, tk.END)

    conn = sqlite3.connect("grades.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM grades WHERE date BETWEEN ? AND ?", (start_date, end_date)
    )

    for row in cursor.fetchall():
        listbox.insert(tk.END, row)

    conn.close()


def clear_entries():
    surname_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)


root = tk.Tk()
root.title("Журнал успеваемости")
root.geometry("800x800")

font_label = font.Font(family="Helvetica", size=10)
font_entry = font.Font(family="Helvetica", size=10)
font_button = font.Font(family="Helvetica", size=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Фамилия:", font=font_label).grid(row=0, column=0, padx=5, pady=5)
surname_entry = tk.Entry(frame, font=font_entry)
surname_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Предмет:", font=font_label).grid(row=1, column=0, padx=5, pady=5)
subject_entry = tk.Entry(frame, font=font_entry)
subject_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Оценка:", font=font_label).grid(row=2, column=0, padx=5, pady=5)
grade_entry = tk.Entry(frame, font=font_entry)
grade_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Дата:", font=font_label).grid(
    row=3, column=0, padx=(5, 10), pady=(5, 10)
)

date_entry = DateEntry(frame, font=font_entry, date_pattern="dd.mm.yyyy")
date_entry.grid(row=3, column=1, padx=(5, 10), pady=(5, 10))

btn_add = tk.Button(root, text="Добавить оценку", command=add_grade, font=font_button)
btn_add.pack(pady=(10, 5))

btn_delete = tk.Button(
    root, text="Удалить оценку", command=delete_grade, font=font_button
)
btn_delete.pack(pady=(0, 10))

tk.Label(root, text="Поиск:", font=font_label).pack(pady=(10, 5))
search_entry = tk.Entry(root, font=font_entry)
search_entry.pack(pady=(0, 5))

btn_search = tk.Button(
    root, text="Поиск по имени/предмету", command=search_grades, font=font_button
)
btn_search.pack(pady=(0, 10))

tk.Label(root, text="Начальная дата:", font=font_label).pack(pady=(10, 5))
start_date_entry = DateEntry(root, font=font_entry, date_pattern="dd.mm.yyyy")
start_date_entry.pack(pady=(0, 5))

tk.Label(root, text="Конечная дата:", font=font_label).pack(pady=(10, 5))
end_date_entry = DateEntry(root, font=font_entry, date_pattern="dd.mm.yyyy")
end_date_entry.pack(pady=(0, 5))

btn_search_by_date_range = tk.Button(
    root, text="Поиск по диапазону дат", command=search_by_date_range, font=font_button
)
btn_search_by_date_range.pack(pady=(10, 5))

listbox = tk.Listbox(root, width=80)
listbox.pack(pady=(10))

create_db()
check_table_structure()
load_grades()

root.mainloop()
