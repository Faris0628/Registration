import streamlit as st
import pandas as pd
import sqlite3
import re

# Database setup
conn = sqlite3.connect('umpsa_registration.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
    name TEXT, email TEXT, matric TEXT, phone TEXT,
    faculty TEXT, session TEXT, marital_status TEXT)''')
conn.commit()

# Save to CSV
def save_to_csv(data):
    df = pd.DataFrame([data])
    df.to_csv('umpsa_registrations.csv', mode='a', header=False, index=False)

# Save to DB
def save_to_db(data):
    cursor.execute("INSERT INTO registrations VALUES (?, ?, ?, ?, ?, ?, ?)", tuple(data.values()))
    conn.commit()

# Validators
def is_valid_email(email):
    return re.match(r"[^@]+@student\.umpsa\.edu\.my", email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10

# UI
st.set_page_config(page_title="UMPSA Event Registration", layout="centered")

page = st.sidebar.selectbox("Navigation", ["Home", "Register", "Confirmation"])

if page == "Home":
    st.image("UMPSAlogo.jpg", width=120)
    st.title("UMPSA Student Innovation Day 2025")
    st.subheader("Welcome to the official event registration system")
    st.write("Please proceed to register for the event by selecting **Register** from the menu.")

elif page == "Register":
    st.header("Registration Form - UMPSA Student Innovation Day 2025")
    with st.form("reg_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Student Email (@student.umpsa.edu.my)")
        matric = st.text_input("Matric Number")
        phone = st.text_input("Phone Number")
        faculty = st.selectbox("Faculty", ["FTKEE", "FTKMA", "FKEKK", "FTKA", "FIM", "Other"])
        session = st.selectbox("Session", ["Morning", "Afternoon"])
        marital_status = st.radio("Marital Status", ["Single", "Married"])
        submit = st.form_submit_button("Submit")

        if submit:
            if not all([name, email, matric, phone]):
                st.error("Please fill in all required fields.")
            elif not is_valid_email(email):
                st.error("Email must be a valid UMPSA student email.")
            elif not is_valid_phone(phone):
                st.error("Invalid phone number.")
            else:
                data = {
                    "name": name,
                    "email": email,
                    "matric": matric,
                    "phone": phone,
                    "faculty": faculty,
                    "session": session,
                    "marital_status": marital_status
                }
                save_to_csv(data)
                save_to_db(data)
                st.success("Registration submitted successfully!")
                st.info("Please proceed to the Confirmation tab to view your submission.")

elif page == "Confirmation":
    st.header("Confirmation")
    try:
        df = pd.read_csv("umpsa_registrations.csv", header=None,
                         names=["Name", "Email", "Matric", "Phone", "Faculty", "Session", "Marital Status"])
        st.success("Here is your submitted information:")
        st.dataframe(df.tail(1))
    except FileNotFoundError:
        st.warning("No registration data found.")
