import streamlit as st
from streamlit_option_menu import option_menu
import Home
import Add_Book
import Issue_Book
import Edit_Book
import Manage_Members
import Acoount

def apply_custom_css():
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f0f2f6, #ffffff);
    }
    .css-1d391kg { 
        background-color: #283e4a;
        color: white;
    }
    /* Option Menu styling */
    .nav-link {
        color: white !important;
        transition: transform 0.3s ease, color 0.3s ease;
    }
    .nav-link:hover {
        transform: scale(1.1);
        color: #30cf4b !important;
    }
    /* Custom sidebar title */
    .sidebar .sidebar-content h1 {
        color: white;
        font-weight: bold;
    }
    /* Content container styling */
    .reportview-container {
        background: linear-gradient(135deg, #ffffff, #e0f7fa);
    }
    /* Custom button styling */
    .stButton>button {
        background-color: #ff6f61;
        border: none;
        border-radius: 10px;
        padding: 0.5em 1em;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff8a80;
    }
    /* Animated title styling */
    .title-animated {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { color: #283e4a; }
        50% { color: #ffb703; }
        100% { color: #283e4a; }
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()
    
    with st.sidebar:
        st.title("📚 Library Management")
        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "Add Book", "Issue Book", "Edit_Book", "Manage Members", "Acoount"],
            icons=["house", "book", "arrow-right-circle", "arrow-left-circle", "people", "person-circle"],
            menu_icon="menu-button-wide",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#283e4a"},
                "icon": {"color": "white", "font-size": "18px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#ffb703"},
                "nav-link-selected": {"background-color": "#ff6f61"},
            }
        )
    
    st.markdown("<h1 class='title-animated' style='text-align:center;'>Library Management System</h1>", unsafe_allow_html=True)
    
    if selected == "Home":
        Home.app()
    elif selected == "Add Book":
        Add_Book.app()
    elif selected == "Issue Book":
        Issue_Book.app()
    elif selected == "Edit_Book":
        Edit_Book.app()
    elif selected == "Manage Members":
        Manage_Members.app()
    elif selected == "Acoount":
        Acoount.auth_ui()

if __name__ == "__main__":
    main()
