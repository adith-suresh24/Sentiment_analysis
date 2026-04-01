import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

# Load CSV
df = pd.read_csv("social_media_posts_v2.csv")

# Clean text
stop_words = set(stopwords.words('english'))
df['text'] = df['text'].astype(str).apply(
    lambda x: ' '.join(w.lower() for w in x.split() if w.lower() not in stop_words)
)

X = df['text']
y = df['sentiment']

# Stratified split for balance
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# TF-IDF with bigrams
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Model with smoothing
model = MultinomialNB(alpha=0.5)
model.fit(X_train_vec, y_train)

# Accuracy
pred = model.predict(X_test_vec)
print("\nModel Accuracy:", accuracy_score(y_test, pred))

# CSV Graph
counts = df['sentiment'].value_counts()
plt.bar(counts.index, counts.values)
plt.title("CSV Sentiment Distribution")
plt.show()

# User Input
sentence = input("\nEnter your sentence: ")

sentence_vec = vectorizer.transform([sentence])
result = model.predict(sentence_vec)[0]

print("\nYour Sentiment:", result)

labels = ["positive","negative","neutral"]
values = [0,0,0]

if result=="positive":
    values[0]=1
elif result=="negative":
    values[1]=1
else:
    values[2]=1

plt.bar(labels, values)
plt.title("Your Input Sentiment")
plt.show()
