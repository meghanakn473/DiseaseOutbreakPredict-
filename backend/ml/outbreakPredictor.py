from flask import Flask, request, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the app

# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Ensure that 'historicalData' is provided in the correct format
    try:
        data = request.json['historicalData']
        print("Incoming data:", data)  # Debugging line
    except KeyError:
        return jsonify({"error": "Missing 'historicalData' in request body"}), 400

    # Ensure the data contains the expected columns (cases, temperature, humidity, outbreaks)
    required_columns = ['cases', 'temperature', 'humidity', 'outbreaks']
    for column in required_columns:
        if column not in data[0]:
            return jsonify({"error": f"Missing column '{column}' in data"}), 400

    # Create DataFrame from the data
    df = pd.DataFrame(data)
    print("Dataframe:", df)  # Debugging line

    # Define independent variables (X) and target variable (y)
    X = df[['cases', 'temperature', 'humidity']]  # Independent variables
    y = df['outbreaks']  # Dependent variable

    # Train the model
    try:
        model = LinearRegression()
        model.fit(X, y)
    except Exception as e:
        return jsonify({"error": f"Model training failed: {str(e)}"}), 500

    # Get the dynamic input for prediction
    prediction_input = [[data[0]['cases'], data[0]['temperature'], data[0]['humidity']]]  # Using the first row for prediction
    prediction = model.predict(prediction_input)

    print("Prediction:", prediction)  # Debugging line

    # Return prediction response
    return jsonify({
        'predictedCases': int(prediction[0]),
        'riskLevel': 'High' if prediction[0] > 50 else 'Low'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
