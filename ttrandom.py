import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import matplotlib.pyplot as plt

# Load the dataset
file_path = r'C:\Users\PAVANI\OneDrive\Desktop\Major Project\precision-agriculture-using-machine-learning-main\Data\Crop_recommendation.csv'
data = pd.read_csv(file_path)

# Handle missing data if necessary
data.dropna(inplace=True)

# Feature and target separation
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

# Encode target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Build the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Save the model
joblib.dump(rf_model, 'crop_recommendation_rf_model.pkl')

# Save scaler and label encoder
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

# Feature importance visualization
importances = rf_model.feature_importances_
features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
plt.bar(features, importances, color='skyblue')
plt.title('Feature Importances')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.xticks(rotation=45)
plt.show()

# Decode and predict
def predict_crop(features):
    features_scaled = scaler.transform([features])
    prediction = rf_model.predict(features_scaled)
    crop = label_encoder.inverse_transform(prediction)
    return crop[0]

# Example prediction
example_features = [90, 42, 43, 20.8, 82.0, 6.5, 202.9]  # Example input
predicted_crop = predict_crop(example_features)
print(f"Predicted Crop: {predicted_crop}")