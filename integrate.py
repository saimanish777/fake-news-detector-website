from flask import Flask, request, jsonify, render_template_string
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Load the model and vectorizer
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']
    vectorized_text = vectorizer.transform([text])
    prediction = model.predict(vectorized_text)
    output = prediction[0]
    if output == 1:
        result = "Real"
    else:
        result = "Fake"
    return jsonify({'prediction': result})

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trust Verify</title>
    </head>
    <body>
        <h1>Trust Verify</h1>
        <textarea id="text" placeholder="Enter text here"></textarea>
        <button onclick="check()">Check</button>
        <div id="result"></div>

        <script>
            function check() {
                var text = document.getElementById("text").value;
                fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({text: text})
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("result").innerHTML = "Prediction: " + data.prediction;
                })
                .catch(error => console.error('Error:', error));
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)