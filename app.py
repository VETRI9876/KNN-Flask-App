from flask import Flask, request, jsonify, render_template_string
from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

app = Flask(__name__)

# Load dataset
digits = load_digits()
X = digits.data
y = digits.target

# Let's simulate feature selection by taking mean of left and right halves of images
X_custom = np.hstack([
    X[:, :32].mean(axis=1).reshape(-1, 1),
    X[:, 32:].mean(axis=1).reshape(-1, 1)
])

# Train KNN model
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_custom, y)

# Enhanced HTML UI
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>KNN Digit Classifier</title>
    <style>
        body {
            background: linear-gradient(120deg, #f6f9fc, #e9eff5);
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            height: 100vh;
            justify-content: center;
            align-items: center;
        }
        .card {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        input[type=number] {
            padding: 10px;
            width: 80%;
            margin: 10px 0;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        input[type=submit] {
            padding: 12px 25px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        input[type=submit]:hover {
            background-color: #218838;
        }
        h2 {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Predict Digit Using KNN</h2>
        <form method="post" action="/predict">
            <input type="number" step="any" name="feat1" placeholder="Left Half Mean" required value="{{ feat1 or '' }}">
            <input type="number" step="any" name="feat2" placeholder="Right Half Mean" required value="{{ feat2 or '' }}">
            <br>
            <input type="submit" value="Predict Digit">
        </form>
        {% if prediction is not none %}
            <h3>Predicted Digit: {{ prediction }}</h3>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template, prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.is_json:
            data = request.get_json()
            feat1 = float(data['feat1'])
            feat2 = float(data['feat2'])
            prediction = model.predict([[feat1, feat2]])
            return jsonify({'prediction': int(prediction[0])})
        else:
            feat1 = float(request.form['feat1'])
            feat2 = float(request.form['feat2'])
            prediction = model.predict([[feat1, feat2]])
            return render_template_string(html_template, prediction=int(prediction[0]), feat1=feat1, feat2=feat2)
    except Exception as e:
        return render_template_string(html_template, prediction=f"Error: {e}", feat1=request.form.get('feat1', ''), feat2=request.form.get('feat2', ''))

if __name__ == '__main__':
    app.run(debug=True)
