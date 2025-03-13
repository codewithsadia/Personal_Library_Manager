import streamlit as st
import json
import os

# File to store library data
LIBRARY_FILE = "library.txt"

# Initialize the library
if os.path.exists(LIBRARY_FILE):
    with open(LIBRARY_FILE, "r") as file:
        library = json.load(file)
else:
    library = []

# Function to save the library to a file
def save_library():
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file)

# Function to add a book
def add_book(title, author, year, genre, read_status):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read_status": read_status
    }
    library.append(book)
    save_library()
    st.success("Book added successfully!")

# Function to remove a book
def remove_book(title):
    global library
    library = [book for book in library if book["title"].lower() != title.lower()]
    save_library()
    st.success("Book removed successfully!")

# Function to search for a book
def search_books(query, search_by):
    results = []
    for book in library:
        if search_by == "title" and query.lower() in book["title"].lower():
            results.append(book)
        elif search_by == "author" and query.lower() in book["author"].lower():
            results.append(book)
    return results

# Function to display all books
def display_books():
    if not library:
        st.write("Your library is empty.")
    else:
        for i, book in enumerate(library, 1):
            read_status = "Read" if book["read_status"] else "Unread"
            st.write(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

# Function to display statistics
def display_statistics():
    total_books = len(library)
    read_books = sum(book["read_status"] for book in library)
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.1f}%")

# Streamlit UI
st.title("💥 Personal Library Manager 📚")

# Custom CSS for background color
st.markdown("""
    <style>
    .main {
        background-color: #333333;
        color: white;
    }
    .stSidebar {
        background-color: #333333;
    }
    </style>
    """, unsafe_allow_html=True)

# Menu options
menu = st.sidebar.selectbox(
    "Menu",
    ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
)

if menu == "Add a Book":
    st.header("📖 Add a Book 🎉")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1800, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        if title and author and year and genre:
            add_book(title, author, year, genre, read_status)
        else:
            st.error("Please fill in all fields.")

elif menu == "Remove a Book":
    st.header("Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        if title:
            remove_book(title)
        else:
            st.error("Please enter a title.")

elif menu == "Search for a Book":
    st.header("Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author"])
    query = st.text_input(f"Enter the {search_by.lower()}")
    if st.button("Search"):
        if query:
            results = search_books(query, search_by.lower())
            if results:
                st.write("Matching Books:")
                for i, book in enumerate(results, 1):
                    read_status = "Read" if book["read_status"] else "Unread"
                    st.write(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
            else:
                st.write("No matching books found.")
        else:
            st.error("Please enter a search term.")

elif menu == "Display All Books":
    st.header("Your Library")
    display_books()

elif menu == "Display Statistics":
    st.header("Library Statistics")
    display_statistics()

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Made by ❤️ Sadia Imran")