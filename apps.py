import streamlit as st
import pandas as pd

# Function to load data from CSV
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Function to find hospitals with the required blood units
def find_hospitals(df, blood_type, required_units):
    available_hospitals = df[df[blood_type] >= required_units]
    return available_hospitals[['Hospital Name', blood_type]]

# Path to your CSV file
file_path = 'datablood.csv'

# Load the data
df = load_data(file_path)

# Streamlit app
st.title('Blood Unit Availability Search')

# Initialize session state
if 'available_hospitals' not in st.session_state:
    st.session_state.available_hospitals = None
if 'blood_type' not in st.session_state:
    st.session_state.blood_type = None
if 'required_units' not in st.session_state:
    st.session_state.required_units = 0

# Select blood type
st.session_state.blood_type = st.selectbox('Select Blood Type', df.columns[2:10].tolist(), index=df.columns[2:10].tolist().index(st.session_state.blood_type) if st.session_state.blood_type else 0)

# Input required units
st.session_state.required_units = st.number_input('Required Units', min_value=0, value=st.session_state.required_units)

# Search button
if st.button('Search'):
    df = load_data(file_path)  # Load data each time search is clicked
    st.session_state.available_hospitals = find_hospitals(df, st.session_state.blood_type, st.session_state.required_units)
    
    if not st.session_state.available_hospitals.empty:
        st.write('Hospitals with the required blood units:')
        st.write(st.session_state.available_hospitals)
    else:
        st.write('No hospitals found with the required blood units.')

# Optionally, add functionality to update the data
if st.sidebar.button("Reload Data"):
    df = load_data(file_path)
    st.sidebar.write("Data reloaded!")

