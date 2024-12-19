import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import random
import json

# Database of books (unchanged)
books = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Classic", "read": False},
    {"id": 2, "title": "1984", "author": "George Orwell", "category": "Dystopian", "read": False},
    {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen", "category": "Romance", "read": False},
    {"id": 4, "title": "The Hunger Games", "author": "Suzanne Collins", "category": "Young Adult", "read": False},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Classic", "read": False},
    {"id": 6, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic", "read": False},
    {"id": 7, "title": "Brave New World", "author": "Aldous Huxley", "category": "Dystopian", "read": False},
    {"id": 8, "title": "Jane Eyre", "author": "Charlotte Bronte", "category": "Romance", "read": False},
    {"id": 9, "title": "The Fault in Our Stars", "author": "John Green", "category": "Young Adult", "read": False},
    {"id": 10, "title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy", "read": False},
    {"id": 11, "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "category": "Fantasy", "read": False},
    {"id": 12, "title": "The Da Vinci Code", "author": "Dan Brown", "category": "Thriller", "read": False},
    {"id": 13, "title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "category": "Thriller", "read": False},
    {"id": 14, "title": "The Alchemist", "author": "Paulo Coelho", "category": "Philosophy", "read": False},
    {"id": 15, "title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "category": "Philosophy", "read": False},
]

def display_books():
    book_list.delete(0, tk.END)
    for book in books:
        status = "Read" if book["read"] else "Unread"
        book_list.insert(tk.END, f"{book['id']}. {book['title']} by {book['author']} - {book['category']} ({status})")

# Function to export only added books and read status to a file
def export_books():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if not file_path:
        return
    try:
        # Only save books that are marked as read or were added to the list
        books_to_export = [book for book in books if book["read"] or book["id"] > 15]
        with open(file_path, "w") as file:
            json.dump(books_to_export, file, indent=10)
        messagebox.showinfo("Success", "Book list successfully exported.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while exporting: {e}")

# Function to import book list from a file and update the current session
def import_books():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not file_path:
        return
    try:
        with open(file_path, "r") as file:
            imported_books = json.load(file)
        if isinstance(imported_books, list) and all("id" in book and "title" in book for book in imported_books):
            global books
            # Update the current session with imported books
            existing_ids = {book["id"] for book in books}
            for book in imported_books:
                if book["id"] not in existing_ids:
                    books.append(book)
                else:
                    # Update read status if the book already exists
                    for existing_book in books:
                        if existing_book["id"] == book["id"]:
                            existing_book["read"] = book["read"]
                            break
            display_books()
            messagebox.showinfo("Success", "Book list successfully imported.")
        else:
            messagebox.showwarning("Warning", "Invalid file format.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while importing: {e}")


def mark_as_read():
    try:
        selection = book_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to mark as read.")
            return

        selected = book_list.get(selection)
        book_id = int(selected.split(".")[0])
        for book in books:
            if book["id"] == book_id:
                book["read"] = True
                messagebox.showinfo("Success", f"Marked '{book['title']}' as read.")
                display_books()
                return
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def mark_as_unread():
    try:
        selection = book_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to mark as unread.")
            return

        selected = book_list.get(selection)
        book_id = int(selected.split(".")[0])
        for book in books:
            if book["id"] == book_id:
                book["read"] = False
                messagebox.showinfo("Success", f"Marked '{book['title']}' as unread.")
                display_books()
                return
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def get_recommendations():
    read_categories = {book["category"] for book in books if book["read"]}

    # If no books have been read, recommend "1984"
    if not read_categories:
        special_recommendation = next((book for book in books if book["title"] == "1984"), None)
        if special_recommendation:
            rec_list.delete(0, tk.END)
            rec_list.insert(
                tk.END,
                f"{special_recommendation['title']} by {special_recommendation['author']} ({special_recommendation['category']})"
            )
        return

    # Normal recommendation logic
    recommendations = [book for book in books if book["category"] in read_categories and not book["read"]]
    if not recommendations:
        messagebox.showinfo("No Recommendations", "No more books to recommend in your preferred categories.")
        return

    recommendation = random.choice(recommendations)
    rec_list.delete(0, tk.END)
    rec_list.insert(
        tk.END,
        f"{recommendation['title']} by {recommendation['author']} ({recommendation['category']})"
    )

def add_book():
    # Create a new window for adding a book
    add_window = tk.Toplevel(root)
    add_window.title("Add New Book")

    # Book details entry fields
    tk.Label(add_window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(add_window, width=30)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Author:").grid(row=1, column=0, padx=5, pady=5)
    author_entry = tk.Entry(add_window, width=30)
    author_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Category:").grid(row=2, column=0, padx=5, pady=5)
    category_entry = tk.Entry(add_window, width=30)
    category_entry.grid(row=2, column=1, padx=5, pady=5)

    def submit_book():
        title = title_entry.get().strip()
        author = author_entry.get().strip()
        category = category_entry.get().strip()

        if not title or not author or not category:
            messagebox.showwarning("Warning", "Please fill in all fields.", parent=add_window)
            return

        new_id = max(book["id"] for book in books) + 1
        new_book = {
            "id": new_id,
            "title": title,
            "author": author,
            "category": category,
            "read": False
        }
        books.append(new_book)
        messagebox.showinfo("Success", f"Added '{title}' to the database.", parent=add_window)
        add_window.destroy()
        display_books()

    submit_btn = tk.Button(add_window, text="Add Book", command=submit_book)
    submit_btn.grid(row=3, column=0, columnspan=2, pady=10)

# Create main application window
root = tk.Tk()
root.title("Book Recommender")

# Configure grid layout for centering
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)

# Title Label
title_label = tk.Label(root, text="Book Recommender", font=("Arial", 18, "bold"), fg="blue")
title_label.grid(row=0, column=0, pady=10)

# Book List Display
book_frame = tk.Frame(root)
book_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

book_list = tk.Listbox(book_frame, height=15, width=80, justify="center")
book_list.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(book_frame, orient="vertical", command=book_list.yview)
scrollbar.pack(side="right", fill="y")
book_list.config(yscrollcommand=scrollbar.set)

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, pady=10, sticky="ew")

mark_read_btn = tk.Button(button_frame, text="Mark as Read", command=mark_as_read)
mark_read_btn.pack(side="left", padx=10)

mark_unread_btn = tk.Button(button_frame, text="Mark as Unread", command=mark_as_unread)
mark_unread_btn.pack(side="left", padx=10)

recommend_btn = tk.Button(button_frame, text="Get Recommendation", command=get_recommendations)
recommend_btn.pack(side="left", padx=10)

add_book_btn = tk.Button(button_frame, text="Add Book", command=add_book)
add_book_btn.pack(side="left", padx=10)

import_btn = tk.Button(button_frame, text="Import", command=import_books)
import_btn.pack(side="left", padx=10)

export_btn = tk.Button(button_frame, text="Export", command=export_books)
export_btn.pack(side="left", padx=10)


# Recommendations Section
rec_label = tk.Label(root, text="Recommendation:", font=("Arial", 14) , fg="red")
rec_label.grid(row=3, column=0, pady=10)

rec_list = tk.Listbox(root, height=3, width=80, justify="center")
rec_list.grid(row=4, column=0, pady=10, padx=20, sticky="nsew")

# Initialize the book list
display_books()

# Run the main event loop
root.mainloop()

