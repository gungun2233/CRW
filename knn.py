import streamlit as st
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# Load the Breast Cancer dataset
breast_cancer = load_breast_cancer()
data = pd.DataFrame(data=breast_cancer.data, columns=breast_cancer.feature_names)
data['target'] = breast_cancer.target

# Split the data into training and testing sets
X = data.drop(columns='target')
y = data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the KNN classifier
n_neighbors = 5
knn = KNeighborsClassifier(n_neighbors=n_neighbors)
knn.fit(X_train_scaled, y_train)

# Title
st.title("Breast Cancer Prediction using KNN")

# Explanation of Malignant and Benign
st.write("""
### Malignant vs Benign
- **Malignant**: Cancerous and potentially dangerous
- **Benign**: Non-cancerous and generally less dangerous
""")

# User input for predictions
st.header("Input Features")
user_input = {}
for feature in breast_cancer.feature_names:
    user_input[feature] = st.number_input(feature, value=float(X_train[feature].mean()))

# Convert user input to DataFrame
user_input_df = pd.DataFrame(user_input, index=[0])

# Standardize the user input
user_input_scaled = scaler.transform(user_input_df)

# Predict button
if st.button("Predict"):
    user_prediction = knn.predict(user_input_scaled)
    prediction_label = "Malignant" if user_prediction[0] == 0 else "Benign"
    st.write(f"### Prediction: {prediction_label}")
