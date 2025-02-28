import streamlit as st
import joblib
import numpy as np

# Load the trained model, scaler, and label encoder
rf_model = joblib.load('crop_recommendation_rf_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Function to predict crop based on user input
def predict_crop(features):
    features_scaled = scaler.transform([features])
    prediction = rf_model.predict(features_scaled)
    crop = label_encoder.inverse_transform(prediction)
    return crop[0]

# Title of the web app
st.title("Crop Recommendation System")

# Display input fields for the user
st.header("Enter the soil and climate features:")

# Use float values for min_value and max_value for consistency
N = st.number_input("Nitrogen (N) content", min_value=0.0, max_value=200.0, value=90.0)
P = st.number_input("Phosphorus (P) content", min_value=0.0, max_value=200.0, value=42.0)
K = st.number_input("Potassium (K) content", min_value=0.0, max_value=200.0, value=43.0)
temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=20.8)
humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=82.0)
ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5)
rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=1000.0, value=202.9)

# Create a list of the user input features
user_features = [N, P, K, temperature, humidity, ph, rainfall]

# Predict button
if st.button("Predict Crop"):
    predicted_crop = predict_crop(user_features)
    st.subheader(f"Recommended Crop: {predicted_crop}")
