# Required libraries import
import streamlit as st             # Streamlit for UI
import sqlite3                    # SQLite for local database
import pandas as pd               # Pandas for data handling
import requests                   # For API requests (book recommendations)
import plotly.graph_objs as go    # Plotly for interactive charts

# -------------------------------------------
# Database setup and connection
conn = sqlite3.connect("library.db", check_same_thread=False)  # Create or connect to SQLite database
cursor = conn.cursor()                                         # Create cursor for executing queries

# Create table if it does not exist already
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique ID for each book
        title TEXT NOT NULL,                    -- Book title
        author TEXT NOT NULL,                   -- Book author
        year INTEGER,                           -- Publication year
        genre TEXT,                             -- Book genre
        read_status BOOLEAN                     -- Read status (True/False)
    )
''')
conn.commit()  # Save the table creation

# -------------------------------------------
# Function to add a book to database
def add_book(title, author, year, genre, read_status):
    cursor.execute('''
        INSERT INTO books (title, author, year, genre, read_status)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, author, year, genre, read_status))
    conn.commit()  # Save new book
    st.success("✅ Book added successfully!")

# Function to remove a book by title
def remove_book(title):
    cursor.execute('DELETE FROM books WHERE LOWER(title) = LOWER(?)', (title,))
    conn.commit()  # Save changes
    st.success("🗑️ Book removed successfully!")

# Function to search for books
def search_books(query, search_by):
    if search_by == "title":
        cursor.execute("SELECT * FROM books WHERE LOWER(title) LIKE ?", ('%' + query.lower() + '%',))
    else:
        cursor.execute("SELECT * FROM books WHERE LOWER(author) LIKE ?", ('%' + query.lower() + '%',))
    return cursor.fetchall()  # Return matching books

# Function to fetch all books from database
def fetch_all_books():
    cursor.execute("SELECT * FROM books")
    return cursor.fetchall()

# Function to display basic statistics
def display_statistics():
    cursor.execute("SELECT COUNT(*) FROM books")
    total = cursor.fetchone()[0]  # Total books
    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read = cursor.fetchone()[0]   # Read books
    percent = (read / total * 100) if total > 0 else 0  # Read percentage
    st.metric("Total Books", total)
    st.metric("Read Percentage", f"{percent:.1f}%")

# Function to export books in CSV or Excel format
def export_books(format):
    books = fetch_all_books()
    df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Year", "Genre", "Read"])
    if format == "CSV":
        csv = df.to_csv(index=False).encode("utf-8")  # Convert to CSV
        st.download_button("⬇️ Download CSV", csv, file_name="library.csv", mime="text/csv")
    elif format == "Excel":
        excel = df.to_excel(index=False, engine='openpyxl')  # Convert to Excel
        st.download_button("⬇️ Download Excel", excel, file_name="library.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# -------------------------------------------
# Streamlit Page Setup
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")  # Set page title and layout

# Custom CSS for dark mode
st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: #f0f0f0;
    }
    .stApp {
        background-color: #1e1e1e;
        color: #f0f0f0;
    }
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div {
        background-color: #333;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title of the app
st.title("📚 Personal Library Manager 📖")

# Sidebar menu
menu = st.sidebar.selectbox(
    "📌 Menu",
    ["Add a Book", "Remove a Book", "Search", "Library Overview", "Statistics", "Export", "Book Recommendations"]
)

# -------------------------------------------
# Menu: Add Book
if menu == "Add a Book":
    st.header("➕ Add a New Book")
    col1, col2 = st.columns(2)  # Split UI in two columns
    with col1:
        title = st.text_input("📖 Book Title")
        author = st.text_input("✍️ Author")
        genre = st.text_input(" 📁 Genre")
    with col2:
        year = st.number_input("📅 Year", min_value=1800, max_value=2100, value=2024)
        read_status = st.checkbox(" ✅ Mark as Read")

    if st.button(" ➕ Add Book"):
        if title and author and genre:
            add_book(title, author, year, genre, read_status)
        else:
            st.error("⚠️ Please fill in all fields.")

# Menu: Remove Book
elif menu == "Remove a Book":
    st.header("🗑️ Remove Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        if title:
            remove_book(title)
        else:
            st.error("⚠️ Please enter a title.")

# Menu: Search Book
elif menu == "Search":
    st.header("🔍 Search for Books")
    search_by = st.radio("Search by", ["Title", "Author"])
    query = st.text_input(f"Enter {search_by}")
    if st.button("Search"):
        if query:
            results = search_books(query, search_by.lower())
            if results:
                st.write("### 🔎 Results")
                for i, book in enumerate(results, 1):
                    status = "✅ Read" if book[5] else "📖 Unread"
                    st.write(f"{i}. **{book[1]}** by *{book[2]}* ({book[3]}) - {book[4]} - {status}")
            else:
                st.warning("No matching books found.")
        else:
            st.error("⚠️ Enter a search query.")

# Menu: Show All Books with Sorting/Filtering
elif menu == "Library Overview":
    st.header("📖 Full Library")
    all_books = fetch_all_books()

    if not all_books:
        st.info("Library is empty.")
    else:
        df = pd.DataFrame(all_books, columns=["ID", "Title", "Author", "Year", "Genre", "Read"])
        read_filter = st.selectbox("📌 Filter by Read Status", ["All", "Read", "Unread"])
        sort_by = st.selectbox("↕️ Sort by", ["Title", "Author", "Year"])

        # Apply filtering
        if read_filter == "Read":
            df = df[df["Read"] == 1]
        elif read_filter == "Unread":
            df = df[df["Read"] == 0]

        # Apply sorting
        df = df.sort_values(by=sort_by)
        st.dataframe(df.drop("ID", axis=1), use_container_width=True)

# Menu: Show Statistics with Charts
elif menu == "Statistics":
    st.header("📊 Library Stats & Progress")

    all_books = fetch_all_books()
    df = pd.DataFrame(all_books, columns=["ID", "Title", "Author", "Year", "Genre", "Read"])

    # Pie Chart for read/unread books
    st.subheader("📈 Reading Progress")
    read = df["Read"].sum()
    unread = len(df) - read
    pie_data = go.Figure(data=[go.Pie(labels=["Read", "Unread"], values=[read, unread], hole=.4)])
    st.plotly_chart(pie_data)

    # Bar Chart for genre-wise distribution
    st.subheader("📚 Genre-wise Distribution")
    genre_df = df.groupby("Genre").size().reset_index(name="Count")
    if not genre_df.empty:
        st.bar_chart(genre_df.set_index("Genre"))

    # Show total stats
    display_statistics()

# Menu: Export
elif menu == "Export":
    st.header("⬇️ Export Your Library")
    export_format = st.selectbox("Choose Format", ["CSV", "Excel"])
    export_books(export_format)

# Menu: Book Recommendations via OpenLibrary API
elif menu == "Book Recommendations":
    st.header("📚 Book Recommendations")

    genre = st.selectbox("Choose a genre", ["fiction", "fantasy", "mystery", "history", "romance", "science"])

    if st.button("Get Recommendations"):
        with st.spinner("Fetching book recommendations..."):
            try:
                response = requests.get(f"https://openlibrary.org/subjects/{genre}.json?limit=5")
                data = response.json()

                if 'works' in data:
                    st.success(f"📚 Top Books in {genre.title()}:")
                    for book in data['works']:
                        title = book['title']
                        authors = ", ".join([a['name'] for a in book.get('authors', [])])
                        st.markdown(f"📖 **{title}** by *{authors}*")
                else:
                    st.warning("No books found.")
            except Exception as e:
                st.error("❌ Failed to fetch recommendations.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ by Sadia Imran")
