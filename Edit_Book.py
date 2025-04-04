import streamlit as st
from models import session, Book

def apply_custom_css():
    st.markdown("""
    <style>
    body {
        background: #fefefe;
        font-family: 'Calibri', sans-serif;
    }
    .stButton>button {
        background-color: #6c757d;
        color: white;
        border-radius: 4px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #222;
    }
    </style>
    """, unsafe_allow_html=True)

def app():
    apply_custom_css()
    st.title("📚 Manage Your Books")
    if "user_id" not in st.session_state:
        st.error("You must be logged in to manage your books.")
        return
    current_user_id = st.session_state["user_id"]
    user_books = session.query(Book).filter_by(uploader_user_id=current_user_id).all()
    if not user_books:
        st.info("You have not uploaded any books yet.")
        return
    for book in user_books:
        st.subheader(f"Book: {book.title}")
        st.write(f"**Author:** {book.author}")
        st.write(f"**Year:** {book.year}")
        borrowers_count = len(book.borrowers) if book.borrowers is not None else 0
        st.write(f"**Number of Borrowers:** {borrowers_count}")
        col_edit, col_delete = st.columns(2)
        with col_edit:
            if st.button("Edit Book", key=f"edit_{book.id}"):
                with st.form(key=f"edit_form_{book.id}", clear_on_submit=True):
                    new_title = st.text_input("New Title", value=book.title)
                    new_author = st.text_input("New Author", value=book.author)
                    new_year = st.number_input("New Year", min_value=1000, max_value=2100, value=book.year)
                    submitted = st.form_submit_button("Update Book")
                    if submitted:
                        book.title = new_title
                        book.author = new_author
                        book.year = new_year
                        try:
                            session.commit()
                            st.success("Book updated successfully!")
                            st.experimental_rerun()
                        except Exception as e:
                            session.rollback()
                            st.error(f"Error updating book: {e}")
        with col_delete:
            with st.expander("Delete Book"):
                if st.button("Confirm Delete", key=f"delete_{book.id}"):
                    session.delete(book)
                    try:
                        session.commit()
                        st.success(f"Book '{book.title}' deleted successfully!")
                        st.experimental_rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error deleting book: {e}")
        st.markdown("---")

if __name__ == "__main__":
    app()
