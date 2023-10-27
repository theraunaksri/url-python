import string
import random
import tkinter as tk
import sqlite3
from tkinter import messagebox

app = tk.Tk()
app.title("URL Shortener")

# SQLite database configuration
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS URL (
            id INTEGER PRIMARY KEY,
            original_url TEXT NOT NULL,
            short_url TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def shorten_url():
    original_url = url_entry.get()
    if original_url:
        short_url = generate_short_url()
        while True:
            cursor.execute('SELECT * FROM URL WHERE short_url = ?', (short_url,))
            existing_entry = cursor.fetchone()
            if not existing_entry:
                break
            short_url = generate_short_url()

        cursor.execute('INSERT INTO URL (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
        conn.commit()
        short_url_label.config(text=f'Short URL: {short_url}')
    else:
        messagebox.showerror("Error", "Please enter a valid URL.")

def redirect_to_original():
    short_url = short_url_entry.get()
    cursor.execute('SELECT original_url FROM URL WHERE short_url = ?', (short_url,))
    entry = cursor.fetchone()
    if entry:
        original_url_label.config(text=f'Original URL: {entry[0]}')
    else:
        original_url_label.config(text="URL not found")

# Create the database tables
create_tables()

# GUI components
url_label = tk.Label(app, text="Enter URL:")
url_label.pack()
url_entry = tk.Entry(app)
url_entry.pack()

shorten_button = tk.Button(app, text="Shorten URL", command=shorten_url)
shorten_button.pack()

short_url_label = tk.Label(app, text="")
short_url_label.pack()

short_url_label = tk.Label(app, text="Enter Short URL:")
short_url_label.pack()
short_url_entry = tk.Entry(app)
short_url_entry.pack()

redirect_button = tk.Button(app, text="Redirect to Original URL", command=redirect_to_original)
redirect_button.pack()

original_url_label = tk.Label(app, text="")
original_url_label.pack()

app.mainloop()
