from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# Example data
examples = [
    {"text": "chandu is a very good boy", "label": "Real"},
    {"text": "chandu is the worst boy", "label": "Fake"},
    {"text": "chandu is a good and loyal friend.", "label": "Real"},
    {"text": "Chandu has a lot of arrogance", "label": "Fake"},
    {"text": "saimanish is a great boy","label":"Real"},
]

# Vectorize the text data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform([example["text"] for example in examples])

# Train a simple Naive Bayes model
cl = MultinomialNB()
cl.fit(X, [example["label"] == "Real" for example in examples])

@app.route('/predict', methods=['POST'])
def predict():
    text = request.json['text']
    X_new = vectorizer.transform([text])
    prediction = cl.predict(X_new)
    confidence = cl.predict_proba(X_new)[0][1] if prediction else cl.predict_proba(X_new)[0][0]
    result = "Real" if prediction else "Fake"
    return jsonify({'prediction': result, 'confidence': f"{confidence:.2f}"})

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/')
def index():
    return render_template_string(open('meta2.html').read())