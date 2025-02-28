import requests
import joblib
import numpy as np

# Load the trained model and preprocessors
rf_model = joblib.load("crop_recommendation_rf_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# ThingSpeak API details
THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"
THINGSPEAK_READ_API_KEY = "YOUR_READ_API_KEY"
URL = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?api_key={THINGSPEAK_READ_API_KEY}&results=1"

# Fetch latest data from ThingSpeak
response = requests.get(URL)
data = response.json()

if "feeds" in data and len(data["feeds"]) > 0:
    latest_entry = data["feeds"][0]

    # Extract sensor values
    nitrogen = float(latest_entry.get("field1", 0))
    phosphorus = float(latest_entry.get("field2", 0))
    potassium = float(latest_entry.get("field3", 0))
    temperature = float(latest_entry.get("field4", 0))
    humidity = float(latest_entry.get("field5", 0))
    ph = float(latest_entry.get("field6", 0))
    rainfall = float(latest_entry.get("field7", 0))

    # Prepare input data
    input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

    # Scale the input
    input_data_scaled = scaler.transform(input_data)

    # Make prediction
    predicted_label = rf_model.predict(input_data_scaled)

    # Convert label to crop name
    predicted_crop = label_encoder.inverse_transform(predicted_label)[0]

    print(f"Predicted Crop: {predicted_crop}")
