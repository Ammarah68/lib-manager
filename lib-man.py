
import streamlit as st
import json
import os

DATA_FILE = "library.json"

# ---------------------- Load/Save Functions ----------------------
def load_library():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_library(library):
    with open(DATA_FILE, "w") as f:
        json.dump(library, f, indent=4)

# ---------------------- UI Functions ----------------------
def display_book(book):
    read_status = "✅ Read" if book['read'] else "📖 Unread"
    st.write(f"**Title:** {book['title']}  \n**Author:** {book['author']}  \n**Year:** {book['year']}  \n**Genre:** {book['genre']}  \n**Status:** {read_status}")
    st.markdown("---")

def display_statistics(library):
    total = len(library)
    read = sum(1 for b in library if b['read'])
    percentage = (read / total) * 100 if total else 0
    st.metric("📚 Total Books", total)
    st.metric("✅ Percentage Read", f"{percentage:.2f}%")

# ---------------------- Main ----------------------
st.set_page_config(page_title="📚 Library Manager", page_icon="📘")
st.title("📘 Personal Library Manager")

library = load_library()

menu = st.sidebar.selectbox("📖 Menu", ["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics"])

# ---------------------- Add Book ----------------------
if menu == "Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?", value=False)
    
    if st.button("Add Book"):
        if title and author and genre:
            new_book = {
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": read
            }
            library.append(new_book)
            save_library(library)
            st.success("Book added successfully!")
        else:
            st.error("Please fill in all fields!")

# ---------------------- Remove Book ----------------------
elif menu == "Remove Book":
    st.header("🗑️ Remove a Book")
    titles = [book['title'] for book in library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book['title'] != book_to_remove]
            save_library(library)
            st.success(f"Removed '{book_to_remove}' successfully.")
    else:
        st.info("No books in your library yet.")

# ---------------------- Search Book ----------------------
elif menu == "Search Book":
    st.header("🔍 Search Books")
    keyword = st.text_input("Enter title or author")
    if keyword:
        results = [book for book in library if keyword.lower() in book['title'].lower() or keyword.lower() in book['author'].lower()]
        if results:
            for book in results:
                display_book(book)
        else:
            st.warning("No books found matching your search.")

# ---------------------- Display All ----------------------
elif menu == "Display All Books":
    st.header("📚 All Books")
    if library:
        for book in library:
            display_book(book)
    else:
        st.info("Your library is empty.")

# ---------------------- Stats ----------------------
elif menu == "Statistics":
    st.header("📈 Library Statistics")
    display_statistics(library)
