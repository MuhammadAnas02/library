import streamlit as st
import base64
from models import session, Book

def apply_custom_css():
    st.markdown("""
    <style>
    body {
        background: #eef2f3;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 0.5em;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #222;
    }
    </style>
    """, unsafe_allow_html=True)

def app():
    apply_custom_css()
    if not st.session_state.get("logged_in"):
        st.warning("⚠️ You must be logged in to add a book.")
        return
    st.title("📖 Add a New Book")
    book_title = st.text_input("Book Title")
    author_name = st.text_input("Author Name")
    book_year = st.number_input("Year of Publication", min_value=1000, max_value=2100, step=1)
    pdf_file = st.file_uploader("Upload Book PDF", type=["pdf"])
    if st.button("Add Book"):
        uploader_id = st.session_state["user_id"]
        pdf_filename = None
        pdf_data = None
        if pdf_file is not None:
            pdf_filename = pdf_file.name
            pdf_data = pdf_file.read()
        new_book = Book(
            title=book_title,
            author=author_name,
            year=book_year,
            uploader_user_id=uploader_id,
            pdf_filename=pdf_filename,
            pdf_data=pdf_data
        )
        session.add(new_book)
        try:
            session.commit()
            st.success(f"📚 Book '{book_title}' by {author_name} added successfully!")
        except Exception as e:
            session.rollback()
            st.error(f"Error adding book: {e}")

if __name__ == "__main__":
    app()
