import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download the dataset (you can use any dataset you prefer)
url = "https://raw.githubusercontent.com/KShriram/fakenewsnet/master/fakenewsnet.csv"
df = pd.read_csv(url)

# Preprocess the data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha()]
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]
    return ' '.join(tokens)

df['text'] = df['text'].apply(preprocess_text)

# Save the preprocessed data
df.to_csv('preprocessed_data.csv', index=False)