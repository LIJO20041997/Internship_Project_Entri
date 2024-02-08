import streamlit as st
import pickle

# Define the Streamlit app title
st.title('Supply Chain Management Prediction')

# Load the pre-trained model
with open('Supply_chain_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define input fields using Streamlit widgets
retail_shop_num = st.number_input('Number of Retail Shops', min_value= 1000, max_value= 15000, value= None)
distributor_num = st.number_input('Number of Distributors', min_value=10, max_value=100, value=None)
dist_from_hub = st.number_input('Distance from Hub', min_value=50, max_value=300, value=None)
workers_num = st.number_input('Number of Workers', min_value=0, max_value=100, value=None)
storage_issue_reported_l3m = st.number_input('Storage Issues Reported Last 3 Months', min_value=0, max_value=50, value=None)
zone_options = ["Zone 1","Zone 2","Zone 3","Zone 4","Zone 5","Zone 6"]
zone = st.selectbox("Regional Zone", zone_options)
grades_options = ["A+", "A", "B+", "B", "C"]  # Define custom grades options
grades = st.selectbox('Gov Certified Grades', grades_options)

# Add a submit button
submit_button = st.button('Submit')

# Function to perform prediction
def predict_production(retail_shop_num, distributor_num, distance, workers, storage_issue_reported, zone, grades):
    try:
        # Define mapping of grades to numeric values
        grade_mapping = {"A+": 0, "A": 1, "B+": 2, "B": 3, "C": 4}
        
        # Convert selected grade to its corresponding numeric value
        numeric_grade = grade_mapping[grades]

        # Perform prediction using the model
        prediction = model.predict([[retail_shop_num, distributor_num, distance, workers, storage_issue_reported, int(zone.split()[-1]), numeric_grade]])

        return prediction[0]  # Assuming the prediction is a single value
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

# Perform prediction when the submit button is clicked
if submit_button:
    prediction_result = predict_production(retail_shop_num, distributor_num, dist_from_hub, workers_num, storage_issue_reported_l3m, zone, grades)
    prediction_result = round(prediction_result,2)
    if prediction_result is not None:
        st.markdown(f'<div style="font-size: 20px; font-weight: bold;">Predicted Product Weight (ton): {prediction_result}</div>', unsafe_allow_html=True)

