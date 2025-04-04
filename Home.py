import streamlit as st
from models import get_all_books

def apply_custom_css():
    st.markdown("""
    <style>
    body {
        background: #f5f7fa;
        font-family: 'Helvetica', sans-serif;
    }
    .stButton>button {
        background-color: #28a745;
        color: white;
        border-radius: 4px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #444;
    }
    </style>
    """, unsafe_allow_html=True)

def app():
    apply_custom_css()
    st.title("🏠 Home - Library Management System")
    books = get_all_books()
    if books:
        for book in books:
            st.subheader(f"📖 {book.title}")
            st.write(f"**Author:** {book.author}")
            st.write(f"**Year:** {book.year}")
            st.write("---")
    else:
        st.warning("No books found in the database.")

if __name__ == "__main__":
    app()
