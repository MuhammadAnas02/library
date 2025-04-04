import streamlit as st
from models import session, Book, User

def apply_custom_css():
    st.markdown("""
    <style>
    body {
        background: #fffafa;
        font-family: 'Verdana', sans-serif;
    }
    .stButton>button {
        background-color: #dc3545;
        color: white;
        border-radius: 4px;
    }
    .stTextInput>div>div>input {
        border-radius: 4px;
        padding: 0.5em;
        border: 1px solid #ccc;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

def app():
    apply_custom_css()
    st.title("📚 Book Issue & View System")
    if "user_id" in st.session_state:
        current_user_id = st.session_state["user_id"]
        current_user = session.query(User).get(current_user_id)
        if not current_user:
            st.error("User session invalid. Please log in again.")
            return
        st.subheader(f"Welcome, {current_user.username} ({current_user.email})")
        st.markdown("---")
        st.header("Issue a Book You Own")
        uploaded_books = session.query(Book).filter_by(uploader_user_id=current_user_id).all()
        if not uploaded_books:
            st.info("You have no uploaded books to issue.")
        else:
            book_titles = [book.title for book in uploaded_books]
            selected_title = st.selectbox("Select a book you own to issue:", book_titles)
            borrower_email = st.text_input("Enter the email of the user to issue the book to:")
            transfer_rights = st.checkbox("Transfer rights (clear previous borrowers)?")
            if st.button("Issue Book"):
                if not borrower_email:
                    st.warning("Please enter the borrower's email.")
                elif borrower_email == current_user.email:
                    st.warning("You cannot issue a book to yourself.")
                else:
                    borrower_user = session.query(User).filter(User.email == borrower_email).first()
                    if not borrower_user:
                        st.error(f"User with email '{borrower_email}' not found.")
                    else:
                        book_to_issue = session.query(Book).filter_by(
                            title=selected_title,
                            uploader_user_id=current_user_id
                        ).first()
                        if not book_to_issue:
                            st.error(f"Book '{selected_title}' not found. Please refresh.")
                        else:
                            if transfer_rights:
                                book_to_issue.borrowers.clear()
                            if borrower_user in book_to_issue.borrowers:
                                st.info(f"{borrower_user.username} already has access to this book.")
                            else:
                                book_to_issue.borrowers.append(borrower_user)
                                try:
                                    session.commit()
                                    st.success(f"Book '{selected_title}' issued to {borrower_user.username} ({borrower_email}).")
                                    st.experimental_rerun()
                                except Exception as e:
                                    session.rollback()
                                    st.error(f"Failed to issue book: {e}")
        st.markdown("---")
        st.header("Books Issued to You")
        borrowed_books = session.query(Book).join(Book.borrowers).filter(User.id == current_user_id).all()
        if not borrowed_books:
            st.info("No book is currently issued to you.")
        else:
            for book in borrowed_books:
                st.write(f"**Title:** {book.title}")
                st.write(f"**Author:** {book.author}")
                st.write(f"**Year:** {book.year}")
                uploader = book.uploader
                if uploader:
                    st.write(f"**Issued by:** {uploader.username} ({uploader.email})")
                else:
                    st.write("**Issued by:** Unknown")
                if book.pdf_data:
                    try:
                        import base64
                        b64_pdf = base64.b64encode(book.pdf_data).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error displaying PDF: {e}")
                else:
                    st.warning("PDF data not available for this book.")
                st.markdown("---")
    else:
        st.error("You must be logged in to issue or view books.")
        st.info("Please log in via the main application page.")

if __name__ == "__main__":
    app()
