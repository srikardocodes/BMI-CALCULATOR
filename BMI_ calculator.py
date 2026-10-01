import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt



DB_NAME = "bmi_records.db"


def create_database():
   
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not create the database.\n\n{error}"
        )


def save_record(name, weight, height, bmi, category):
    
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO bmi_records
            (user_name, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, weight, height, bmi, category, date))

        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not save the BMI record.\n\n{error}"
        )
        return False


def get_user_records(name):
    
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT date, bmi, weight, height, category
            FROM bmi_records
            WHERE user_name = ?
            ORDER BY date
        """, (name,))

        records = cursor.fetchall()
        connection.close()

        return records

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not read BMI records.\n\n{error}"
        )
        return []


def get_users():
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT DISTINCT user_name
            FROM bmi_records
            ORDER BY user_name
        """)

        users = [row[0] for row in cursor.fetchall()]

        connection.close()

        return users

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not retrieve users.\n\n{error}"
        )
        return []



def calculate_bmi(weight, height):
   
    return weight / (height ** 2)


def classify_bmi(bmi):
    
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def get_category_colour(category):
    
    colours = {
        "Underweight": "#3498db",
        "Normal": "#27ae60",
        "Overweight": "#f39c12",
        "Obese": "#e74c3c"
    }

    return colours.get(category, "#333333")




def calculate_and_save():
    
    name = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

   
    if not name:
        messagebox.showwarning(
            "Input Error",
            "Please enter a user's name."
        )
        return

   
    try:
        weight = float(weight_text)

        if weight <= 0:
            messagebox.showwarning(
                "Input Error",
                "Weight must be greater than 0 kg."
            )
            return

    except ValueError:
        messagebox.showwarning(
            "Input Error",
            "Please enter a valid numeric weight."
        )
        return

   
    try:
        height = float(height_text)

        if height <= 0:
            messagebox.showwarning(
                "Input Error",
                "Height must be greater than 0 metres."
            )
            return

    except ValueError:
        messagebox.showwarning(
            "Input Error",
            "Please enter a valid numeric height."
        )
        return

    
    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

  
    result_label.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}",
        foreground=get_category_colour(category)
    )

    
    saved = save_record(
        name,
        weight,
        height,
        bmi,
        category
    )

    if saved:
        messagebox.showinfo(
            "Success",
            f"BMI record saved successfully for {name}."
        )

        update_user_list()


def update_user_list():
    users = get_users()

    user_combobox["values"] = users


def show_history():
   

    name = name_entry.get().strip()

    if not name:
        messagebox.showwarning(
            "Input Error",
            "Please enter a user name."
        )
        return

    records = get_user_records(name)

    if not records:
        messagebox.showinfo(
            "No Records",
            f"No BMI records found for {name}."
        )
        return

   
    for item in history_tree.get_children():
        history_tree.delete(item)

   
    for record in records:
        date, bmi, weight, height, category = record

        history_tree.insert(
            "",
            tk.END,
            values=(
                date,
                f"{bmi:.2f}",
                f"{weight:.1f}",
                f"{height:.2f}",
                category
            )
        )


def select_user(event=None):
    

    selected_user = user_combobox.get()

    if selected_user:
        name_entry.delete(0, tk.END)
        name_entry.insert(0, selected_user)

        show_history()


def show_graph():
    

    name = name_entry.get().strip()

    if not name:
        messagebox.showwarning(
            "Input Error",
            "Please enter a user name."
        )
        return

    records = get_user_records(name)

    if len(records) < 2:
        messagebox.showinfo(
            "Not Enough Data",
            "At least two BMI records are required "
            "to display a trend."
        )
        return

    dates = []
    bmi_values = []

    for record in records:
        date, bmi, weight, height, category = record

        dates.append(
            datetime.strptime(
                date,
                "%Y-%m-%d %H:%M:%S"
            )
        )

        bmi_values.append(bmi)

    
    plt.figure(figsize=(10, 5))

    plt.plot(
        dates,
        bmi_values,
        marker="o",
        linewidth=2,
        color="#3498db"
    )

   
    plt.axhline(
        18.5,
        color="#3498db",
        linestyle="--",
        alpha=0.5,
        label="Underweight limit"
    )

    plt.axhline(
        25,
        color="#27ae60",
        linestyle="--",
        alpha=0.5,
        label="Normal limit"
    )

    plt.axhline(
        30,
        color="#e74c3c",
        linestyle="--",
        alpha=0.5,
        label="Obese limit"
    )

    plt.title(f"BMI Trend for {name}")
    plt.xlabel("Date")
    plt.ylabel("BMI")

    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def clear_fields():
   
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    result_label.config(
        text="Enter your details to calculate BMI.",
        foreground="#333333"
    )

    for item in history_tree.get_children():
        history_tree.delete(item)



create_database()

root = tk.Tk()

root.title("Advanced BMI Health Tracker")
root.geometry("900x700")
root.minsize(800, 600)

root.configure(bg="#f4f6f7")




style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Title.TLabel",
    background="#2c3e50",
    foreground="white",
    font=("Arial", 24, "bold"),
    padding=15
)

style.configure(
    "Heading.TLabel",
    background="#f4f6f7",
    foreground="#2c3e50",
    font=("Arial", 15, "bold")
)

style.configure(
    "TLabel",
    background="#f4f6f7",
    font=("Arial", 11)
)

style.configure(
    "TButton",
    font=("Arial", 10, "bold"),
    padding=8
)

style.configure(
    "Treeview",
    font=("Arial", 10),
    rowheight=28
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)




title_label = ttk.Label(
    root,
    text="BMI Health Tracker",
    style="Title.TLabel"
)

title_label.pack(fill="x")



input_frame = ttk.LabelFrame(
    root,
    text="Personal Information",
    padding=15
)

input_frame.pack(
    fill="x",
    padx=20,
    pady=15
)



ttk.Label(
    input_frame,
    text="User Name:"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

name_entry = ttk.Entry(
    input_frame,
    width=30
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)



ttk.Label(
    input_frame,
    text="Saved Users:"
).grid(
    row=0,
    column=2,
    padx=10,
    pady=10
)

user_combobox = ttk.Combobox(
    input_frame,
    width=25,
    state="readonly"
)

user_combobox.grid(
    row=0,
    column=3,
    padx=10,
    pady=10
)

user_combobox.bind(
    "<<ComboboxSelected>>",
    select_user
)



ttk.Label(
    input_frame,
    text="Weight (kg):"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

weight_entry = ttk.Entry(
    input_frame,
    width=30
)

weight_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)



ttk.Label(
    input_frame,
    text="Height (m):"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)

height_entry = ttk.Entry(
    input_frame,
    width=30
)

height_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)




button_frame = ttk.Frame(root)

button_frame.pack(
    pady=5
)


calculate_button = ttk.Button(
    button_frame,
    text="Calculate & Save",
    command=calculate_and_save
)

calculate_button.grid(
    row=0,
    column=0,
    padx=5
)


history_button = ttk.Button(
    button_frame,
    text="Show History",
    command=show_history
)

history_button.grid(
    row=0,
    column=1,
    padx=5
)


graph_button = ttk.Button(
    button_frame,
    text="View BMI Trend",
    command=show_graph
)

graph_button.grid(
    row=0,
    column=2,
    padx=5
)


clear_button = ttk.Button(
    button_frame,
    text="Clear",
    command=clear_fields
)

clear_button.grid(
    row=0,
    column=3,
    padx=5
)




result_frame = ttk.LabelFrame(
    root,
    text="BMI Result",
    padding=15
)

result_frame.pack(
    fill="x",
    padx=20,
    pady=15
)


result_label = ttk.Label(
    result_frame,
    text="Enter your details to calculate BMI.",
    font=("Arial", 18, "bold")
)

result_label.pack()




history_frame = ttk.LabelFrame(
    root,
    text="BMI History",
    padding=10
)

history_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


columns = (
    "Date",
    "BMI",
    "Weight",
    "Height",
    "Category"
)

history_tree = ttk.Treeview(
    history_frame,
    columns=columns,
    show="headings"
)


for column in columns:
    history_tree.heading(
        column,
        text=column
    )

    history_tree.column(
        column,
        anchor="center"
    )


history_tree.pack(
    fill="both",
    expand=True
)



update_user_list()

root.mainloop()
