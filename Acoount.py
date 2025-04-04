import streamlit as st
import bcrypt
import logging
from models import session, User

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def signup(username, email, password):
    existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return False, "Username or email already exists."
    hashed_pw = hash_password(password)
    new_user = User(username=username, email=email, password=hashed_pw)
    session.add(new_user)
    session.commit()
    logging.info(f"User '{username}' created successfully.")
    return True, "User created successfully! Please log in."

def login(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and check_password(password, user.password):
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["user_id"] = user.id
        logging.info(f"User '{username}' logged in successfully.")
        return True, "Login successful!"
    else:
        return False, "Invalid username or password."

def apply_custom_css():
    st.markdown("""
    <style>
    body {
        background: #f0f2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5em 1em;
    }
    .stTextInput>div>div>input {
        border-radius: 4px;
        border: 1px solid #ccc;
        padding: 0.5em;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

def auth_ui():
    apply_custom_css()
    st.title("🔐 Library Authentication")
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["user_id"] = None
    if st.session_state["logged_in"]:
        st.success(f"Welcome, {st.session_state['username']}!")
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.session_state["user_id"] = None
            st.rerun()
    else:
        auth_choice = st.radio("Choose:", ["Login", "Sign Up"], horizontal=True)
        if auth_choice == "Login":
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                if submitted and username and password:
                    success, message = login(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            with st.form("signup_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submitted = st.form_submit_button("Sign Up")
                if submitted:
                    if not username or not email or not password or not confirm_password:
                        st.warning("Fill in all fields.")
                    elif password != confirm_password:
                        st.error("Passwords do not match!")
                    else:
                        success, message = signup(username, email, password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)

if __name__ == "__main__":
    auth_ui()
