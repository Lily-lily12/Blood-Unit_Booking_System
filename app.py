import pandas as pd
import streamlit as st

# Load the data from the pickle file
df=pd.read_csv('datablood.csv')

# Function to find hospitals with the required blood units
def find_hospitals(df, blood_type, required_units):
    # Filter hospitals where the blood type units are greater than or equal to required units
    available_hospitals = df[df[blood_type] >= required_units]
    
    # Return the hospital names and available units
    return available_hospitals[['Hospital Name', blood_type]]

# Streamlit app
st.title('Blood Unit Availability Checker')

# Select blood type
blood_type = st.selectbox('Select Blood Type', df.columns[1:10].tolist())

# Input required units
required_units = st.number_input('Required Units', min_value=0)

# Search button
if st.button('Search'):
    available_hospitals = find_hospitals(df, blood_type, required_units)
    
    if not available_hospitals.empty:
        st.write('Hospitals with the required blood units:')
        st.write(available_hospitals)
    else:
        st.write('No hospitals found with the required blood units.')

