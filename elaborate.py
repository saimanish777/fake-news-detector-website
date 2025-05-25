from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# Load the trained model and vectorizer
vectorizer = TfidfVectorizer()
cl = MultinomialNB()

# Train the model (you can load a pre-trained model instead)
examples = [
    {"text": "IIT kanpur is one of the best institutes in the nation", "label": "Real"},
    {"text": "IITs are worst colleges on earth", "label": "Fake"},
    # Add more examples here
]
X = vectorizer.fit_transform([example["text"] for example in examples])
cl.fit(X, [example["label"] == "Real" for example in examples])

@app.route('/predict', methods=['POST'])
def predict():
    text = request.get_json()['text']
    X_new = vectorizer.transform([text])
    prediction = cl.predict(X_new)
    confidence = cl.predict_proba(X_new)[0][1] if prediction else cl.predict_proba(X_new)[0][0]
    confidence_level = "Very High" if confidence > 0.95 else "High" if confidence > 0.8 else "Medium" if confidence > 0.5 else "Low"
    result = {
        'prediction': 'Yes' if prediction else 'No',
        'confidence_level': confidence_level,
        'confidence': f"{confidence*100:.2f}%"
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)