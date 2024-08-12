
import streamlit as st
import pandas as pd
import sqlite3

# Load data
@st.cache
def load_data():
    data = pd.read_csv("datablood.csv")
    return data

data = load_data()

conn = sqlite3.connect('blood_requests.db')
c = conn.cursor()

# Create table for storing blood requests
c.execute("CREATE TABLE IF NOT EXISTS requests (hospital_name TEXT, blood_group TEXT, units INTEGER)")

# Filter hospitals based on required blood group and units
st.title("Blood Unit Requirement")
required_units = st.number_input('Enter the number of units required:', min_value=1)
required_blood_group = st.selectbox('Select the blood group required:', data.columns[2:10])

filtered_data = data[data[required_blood_group] >= required_units]

if not filtered_data.empty:
    st.subheader("Hospitals that can fulfill the requirement:")
    st.table(filtered_data[['Hospital Name', required_blood_group]])
else:
    st.subheader("No hospitals can fulfill the requirement at this time.")

# Form for submitting a blood request
st.title("Submit Blood Request")
with st.form(key='blood_request_form'):
    hospital_name = st.selectbox('Select the hospital:', data['Hospital Name'])
    blood_group = st.selectbox('Select the blood group:', data.columns[2:10])
    units = st.number_input('Enter the number of units required:', min_value=1)
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Insert request into the database
        c.execute("INSERT INTO requests (hospital_name, blood_group, units) VALUES (?, ?, ?)",
                  (hospital_name, blood_group, units))
        conn.commit()
        st.success("Blood request submitted successfully!")

# Display stored requests
st.title("Submitted Requests")
requests_data = pd.read_sql('SELECT * FROM requests', conn)
st.table(requests_data)

# Close the database connection
conn.close()
