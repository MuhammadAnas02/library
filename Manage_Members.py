import streamlit as st
from models import session, Book, User

def apply_custom_css():
    st.markdown("""
    <style>
    body {
        background: #fafafa;
        font-family: 'Tahoma', sans-serif;
    }
    .stButton>button {
        background-color: #ff5722;
        color: white;
        border-radius: 4px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

def app():
    apply_custom_css()
    st.title("📊 Manage Book Borrowers")
    if "user_id" not in st.session_state:
        st.error("You must be logged in to view this page.")
        return
    current_user_id = st.session_state["user_id"]
    uploaded_books = session.query(Book).filter_by(uploader_user_id=current_user_id).all()
    if not uploaded_books:
        st.info("You have not uploaded any books.")
        return
    for book in uploaded_books:
        st.subheader(f"Book: {book.title}")
        borrowers = book.borrowers
        if not borrowers:
            st.info("No users have borrowed this book.")
        else:
            for borrower in borrowers:
                col1, col2, col3 = st.columns([3, 3, 2])
                with col1:
                    st.write(f"**User:** {borrower.username}")
                with col2:
                    st.write(f"**Email:** {borrower.email}")
                with col3:
                    if st.button("Remove Access", key=f"remove_{book.id}_{borrower.id}"):
                        if borrower in book.borrowers:
                            book.borrowers.remove(borrower)
                            try:
                                session.commit()
                                st.success(f"Removed access for {borrower.username} from '{book.title}'")
                                st.experimental_rerun()
                            except Exception as e:
                                session.rollback()
                                st.error(f"Error removing access: {e}")

if __name__ == "__main__":
    app()
