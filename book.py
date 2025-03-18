import streamlit as st
import json

# load and save library
def load_library():
    try:
        with open('library.json','r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_library(library):
    with open('library.json','w') as file:
        json.dump(library,file,indent=4)

# initialize library
library = load_library()
st.title('📖 Personal Library Manager')
menu = st.sidebar.radio('select an option',['📚View library','➕📗Add Book','➖📕Remove Book','🔎📘Search Book','🗃️📤Save and exit'])
if menu=='📚View library':
    st.sidebar.header('📚your library')
    if library:
        st.table(library)
    else:
        st.write('📚no book in your library')
# Add Book
elif menu == '➕📗Add Book':
    st.sidebar.header('Add a new book')
    title = st.text_input('Title')
    author = st.text_input('Author')
    year = st.number_input('year',min_value=2000,max_value=2050,step=1)
    genre = st.text_input('Genre')
    read_status = st.checkbox('mark as read')
    if(st.button('➕Add Book')):
        library.append({'title':title,'author':author,'year':year,'genre':genre,'read_status':read_status})
        save_library(library)
        st.success('book added successfully!')
        st.rerun()
# Remove Book
elif menu == '➖📕Remove Book':
    st.sidebar.header('remove a book')
    book_title=[book['title'] for book in library]
    if book_title:
        selected_book = st.selectbox('select a book to remove',book_title)
        if st.button('➖Remove Book'):
            library = [book for book in library if book['title']!=selected_book]
            save_library(library)
            st.success('book removed successfully!')
            st.rerun()
        else:
            if not book_title:
                st.warning('No book in your library, Add some books!')

# Search Book
elif menu == '🔎📘Search Book':
    st.sidebar.header('Search a book')
    search_term = st.text_input('Enter title or author name')
    if st.button('Search'):
        results = [book for book in library if search_term.lower() in book['title'].lower() or search_term.lower() in book['author'].lower()]
        if results:
            st.table(results)
        else:
            st.warning('No book found!')


# save and exit
elif menu == '🗃️📤Save and exit':
    save_library(library)
    st.success('🗃️Library saved successfully!')

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ by Sadia Imran")