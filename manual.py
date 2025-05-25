import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Example data
examples = [
    {"text": "", "label": "Real"},
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

def predict_text():
    text = input("Enter text: ")
    X_new = vectorizer.transform([text])
    prediction = cl.predict(X_new)
    confidence = cl.predict_proba(X_new)[0][1] if prediction else cl.predict_proba(X_new)[0][0]
    result = "Real" if prediction else "Fake"
    print(f"Prediction: {result}")
    print(f"Confidence: {confidence:.2f}")

while True:
    predict_text()
    cont = input("Do you want to continue? (yes/no): ")
    if cont.lower() != "yes":
        break