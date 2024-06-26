import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# Previously created DataFrame
data = {
    'outlook': ['sunny', 'sunny', 'overcast', 'rainy', 'sunny', 'overcast', 'rainy', 'rainy', 'rainy', 'overcast', 'sunny', 'sunny'],
    'humidity': ['high', 'high', 'high', 'high', 'normal', 'normal', 'high', 'normal', 'normal', 'high', 'high', 'normal'],
    'windy': ['weak', 'strong', 'weak', 'weak', 'strong', 'weak', 'strong', 'weak', 'weak', 'strong', 'weak', 'strong'],
    'play': ['no', 'no', 'yes', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'no', 'yes']
}

df = pd.DataFrame(data)

# Encode categorical variables
label_encoders = {}
categorical_columns = ['outlook', 'humidity', 'windy', 'play']

for col in categorical_columns:
    label_encoders[col] = LabelEncoder()
    df[col] = label_encoders[col].fit_transform(df[col])

# Prepare features and target
features_col = ['outlook', 'humidity', 'windy']
X = data[features_col]  # Corrected: data instead of df

y = data['play']  # Corrected: data instead of df

# Create a Decision Tree Classifier
classifier = DecisionTreeClassifier(criterion='gini')
classifier.fit(X, y)  # Train on the entire dataset

# Define function to predict using the trained model
def predict_outcome(outlook, humidity, windy):
    try:
        # Encode user inputs
        outlook_encoded = label_encoders['outlook'].transform([outlook])[0]
        humidity_encoded = label_encoders['humidity'].transform([humidity])[0]
        windy_encoded = label_encoders['windy'].transform([windy])[0]
        
        # Make prediction
        prediction = classifier.predict([[outlook_encoded, humidity_encoded, windy_encoded]])
        
        # Map prediction to readable outcome
        outcome = label_encoders['play'].inverse_transform(prediction)[0]
        
        return outcome
    except ValueError as e:
        st.error(f"Error: {e}. Please enter valid weather conditions.")

# Define the Streamlit app
def main():
    st.title('Weather-Based Play Prediction')
    st.markdown('This app predicts if you can play based on weather conditions.')
    
    # Define categorical options
    outlook_options = label_encoders['outlook'].classes_
    humidity_options = label_encoders['humidity'].classes_
    windy_options = label_encoders['windy'].classes_
    
    # Collect user inputs
    outlook = st.selectbox('Outlook', outlook_options)
    humidity = st.selectbox('Humidity', humidity_options)
    windy = st.selectbox('Windy', windy_options)
    
    # Display prediction button
    if st.button('Predict'):
        predicted_outcome = predict_outcome(outlook, humidity, windy)
        if predicted_outcome is not None:
            st.success(f'Predicted Outcome: {predicted_outcome}')

if __name__ == '__main__':
    main()
