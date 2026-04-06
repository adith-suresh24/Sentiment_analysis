import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import nltk
from nltk.corpus import stopwords
import plotly.express as px

# Download stopwords
try:
    stopwords.words('english')
except:
    nltk.download('stopwords')

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

st.title("🎯 Sentiment Analysis Tool")
st.markdown("Analyze the sentiment of social media posts and custom text")

# Load and train model
@st.cache_resource
def train_model():
    df = pd.read_csv("social_media_posts_v2.csv")
    
    stop_words = set(stopwords.words('english'))
    df['text'] = df['text'].astype(str).apply(
        lambda x: ' '.join(w.lower() for w in x.split() if w.lower() not in stop_words)
    )
    
    X = df['text']
    y = df['sentiment']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    model = MultinomialNB(alpha=0.5)
    model.fit(X_train_vec, y_train)
    
    pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, pred)
    
    return model, vectorizer, df, accuracy

model, vectorizer, df, accuracy = train_model()

# Display dataset stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Model Accuracy", f"{accuracy:.2%}")
with col2:
    st.metric("Total Posts", len(df))
with col3:
    st.metric("Features", vectorizer.get_feature_names_out().shape[0])

# Dataset distribution
st.subheader("Dataset Sentiment Distribution")
sentiment_counts = df['sentiment'].value_counts()
fig = px.bar(
    x=sentiment_counts.index,
    y=sentiment_counts.values,
    labels={'x': 'Sentiment', 'y': 'Count'},
    color=sentiment_counts.index,
    color_discrete_map={'positive': '#00cc00', 'negative': '#ff4444', 'neutral': '#4444ff'}
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# User input section
st.subheader("Test Your Text")
user_input = st.text_area("Enter text to analyze:", placeholder="Type or paste your text here...")

if user_input:
    # Predict sentiment
    text_vec = vectorizer.transform([user_input])
    prediction = model.predict(text_vec)[0]
    
    # Get probabilities
    probabilities = model.predict_proba(text_vec)[0]
    classes = model.classes_
    
    # Display result
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sentiment_emoji = {
            'positive': '😊',
            'negative': '😞',
            'neutral': '😐'
        }
        color_map = {
            'positive': '#00cc00',
            'negative': '#ff4444',
            'neutral': '#4444ff'
        }
        
        st.markdown(f"### Sentiment: **{sentiment_emoji.get(prediction, '')} {prediction.upper()}**")
        st.markdown(f"<p style='color: {color_map.get(prediction, '#000')}; font-weight: bold;'>Prediction confirmed</p>", 
                   unsafe_allow_html=True)
    
    with col2:
        st.info(f"Confidence: **{max(probabilities):.1%}**")
    
    # Show confidence breakdown
    st.subheader("Confidence Breakdown")
    prob_df = pd.DataFrame({
        'Sentiment': classes,
        'Confidence': probabilities
    }).sort_values('Confidence', ascending=False)
    
    fig_prob = px.bar(
        prob_df,
        x='Sentiment',
        y='Confidence',
        color='Sentiment',
        color_discrete_map={'positive': '#00cc00', 'negative': '#ff4444', 'neutral': '#4444ff'},
        labels={'Confidence': 'Confidence Score'}
    )
    st.plotly_chart(fig_prob, use_container_width=True)
