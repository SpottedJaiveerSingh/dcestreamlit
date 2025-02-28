import streamlit as st
import sqlite3 
from streamlit_option_menu import option_menu  # Import option menu

# Function to Connect to Database
def connect_db():
    conn = sqlite3.connect("mydb.db")
    return conn 

# Function to Create Table if Not Exists
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS student(name TEXT, roll TEXT, branch TEXT, password TEXT)')
    conn.commit()
    conn.close()

# Function to Add Record
def add_record(data):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO student (name, roll, branch, password) VALUES (?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

# Function to View Records
def view_records():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    result = cur.fetchall()  # Fixed Typo
    conn.close()
    return result

# Function to Display Records
def display_records():
    data = view_records()
    if data:
        st.write("### Registered Students:")
        for row in data:
            st.write(f"📌 **Name:** {row[0]} | **Roll No:** {row[1]} | **Branch:** {row[2]}")
    else:
        st.warning("No records found.")

# Function for Sign-Up Form
def signup():
    st.title("📝 Student Registration Form")
    
    name = st.text_input("Enter your Name:")
    roll_no = st.text_input("Enter your Roll Number:")
    branch = st.selectbox("Select Your Branch:", ["AIML", "CSE", "ECE", "ME"])
    password = st.text_input("Enter Password:", type="password")
    confirm_password = st.text_input("Re-type Password:", type="password")

    if st.button("Sign Up Now"):
        if not name or not roll_no or not password or not confirm_password:
            st.error("❌ Please fill in all fields!")
        elif password != confirm_password:
            st.error("❌ Passwords do not match!")
        else:
            add_record((name, roll_no, branch, password))
            st.success(f"✅ Welcome, {name}! You have successfully signed up.")

# Create Database Table
create_table()

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  # Required
        options=["Home", "Sign Up", "View Records"],  # Menu Options
        icons=["house", "person-plus", "database"],  # Bootstrap Icons
        menu_icon="cast",  # Main menu icon
        default_index=0,  # Default active menu item
    )

# Page Navigation
if selected == "Home":
    st.title("🏠 Welcome to the Student Registration System")
    st.write("Use the sidebar to navigate.")

elif selected == "Sign Up":
    signup()

elif selected == "View Records":
    st.title("📜 Registered Students")
    display_records()