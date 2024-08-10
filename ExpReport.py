from dotenv import load_dotenv
load_dotenv() ## loading all environment variables

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
import os 

# st.set_page_config(page_title = "Q&A Demo")
# st.header("Gemini LLM Application")
# input = st.text_input("Input: ", key = "input")
# submit = st.button("sumbit the question")


# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Monthly_Expenditure").sheet1

# Streamlit App
st.title("Monthly Expenditure Tracker")

# Data Entry Form
with st.form(key='expense_form'):
    date = st.date_input("Select Date")
    category = st.selectbox("Select Category", ["Food", "Medical", "Investment", "Travel", "Online Purchase", "Home", "Outside Spent", "Fitness", "Children"])
    amount = st.number_input("Enter Amount", min_value=0.0, step=0.1)
    submit_button = st.form_submit_button(label='Submit')

# Handling Form Submission
if submit_button:
    # Append data to Google Sheet
    sheet.append_row([str(date), category, amount])
    st.success(f"Recorded: {category} - ${amount} on {date}")

# Data Visualization
st.header("Expenditure Report")
if st.button("Generate Report"):
    data = pd.DataFrame(sheet.get_all_records())

    if not data.empty:
        # Grouping by Category and Summing Amounts
        category_data = data.groupby('Category')['Amount'].sum()

        # Plotting Pie Chart
        fig, ax = plt.subplots()
        ax.pie(category_data, labels=category_data.index, autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
    else:
        st.write("No data available yet.")
