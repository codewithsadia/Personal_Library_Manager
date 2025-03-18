import json
import os

# Load and save library functions
def load_library():
    if os.path.exists('library.json'):
        with open('library.json', 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open('library.json', 'w') as file:
        json.dump(library, file, indent=4)

# Main function for the library manager
def main():
    library = load_library()

    while True:
        print("""
              Personal Library Manager
             
              1- Add a Book
              2- Remove a Book
              3- view library
              4- search a book
              5- Save and exit
              """)
        choice = input("Select an option (1-5): ")

        if choice == '1':
            title = input("Enter the book title: ")
            author = input("Enter the author's name: ")
            year = input("Enter the year of publication: ")
            genre = input("Enter the genre: ")
            read_status = input("Mark as read? (yes/no): ").lower() == 'yes'
            library.append({
                'title': title,
                'author': author,
                'year': year,
                'genre': genre,
                'read_status': read_status
            })
            print("Book added successfully!")

        elif choice == '2':
            title = input("Enter the title of the book to remove: ")
            library = [book for book in library if book['title'] != title]
            print("Book removed successfully!")

        elif choice == '3':
            if library:
                print("\nYour Library:")
                for book in library:
                    print(f"{book['title']} by {book['author']} ({book['year']}) - Genre: {book['genre']} - Read: {'Yes' if book['read_status'] else 'No'}")
            else:
                print("Your library is empty.")

        elif choice == '4':
            search_term = input("Enter title or author name to search: ")
            results = [book for book in library if search_term.lower() in book['title'].lower() or search_term.lower() in book['author'].lower()]
            if results:
                print("\nSearch Results:")
                for book in results:
                    print(f"{book['title']} by {book['author']} ({book['year']}) - Genre: {book['genre']} - Read: {'Yes' if book['read_status'] else 'No'}")
            else:
                print("No books found!")

        elif choice == '5':
            save_library(library)
            print("Library saved successfully! Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main() 