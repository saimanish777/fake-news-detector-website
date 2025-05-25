import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Example data
examples = [
    {"text": "IIT kanpur is one of the best institutes in the nation", "label": "Real"},
    {"text": "IITs are worst colleges on earth", "label": "Fake"},
    {"text": "The Indian government has launched a new initiative to promote renewable energy", "label": "Real"},
    {"text": "The world is going to end tomorrow", "label": "Fake"},
    {"text": "The Indian economy is expected to grow at a rate of 7% in the coming year", "label": "Real"},
    {"text": "Aliens have landed on Earth", "label": "Fake"}
]

# Vectorize the text data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform([example["text"] for example in examples])

# Train a simple Naive Bayes model
cl = MultinomialNB()
cl.fit(X, [example["label"] == "Real" for example in examples])

# Make predictions
predictions = cl.predict(X)

# Print the results
for i, example in enumerate(examples):
    prediction = "Real" if predictions[i] else "Fake"
    confidence = cl.predict_proba(X)[i][1] if prediction == "Real" else cl.predict_proba(X)[i][0]
    print(f"Example {i+1}: {example['text']}")
    print(f"Prediction: {prediction}")
    print(f"Confidence: {confidence:.2f}")
    print()