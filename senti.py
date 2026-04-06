import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import nltk
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import ttk, messagebox
import threading

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
accuracy = accuracy_score(y_test, pred)
print(f"\nModel Accuracy: {accuracy:.2%}")

# GUI
class SentimentAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sentiment Analysis Tool")
        self.root.geometry("1000x700")
        self.root.config(bg="#f0f0f0")
        
        # Title
        title_frame = tk.Frame(root, bg="#2c3e50")
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="🎯 Sentiment Analysis Tool", 
                              font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(padx=20, pady=10)
        
        # Main container
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Charts
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Dataset distribution chart
        dataset_label = tk.Label(left_frame, text="Dataset Sentiment Distribution", 
                                font=("Helvetica", 12, "bold"), bg="#f0f0f0")
        dataset_label.pack(pady=(0, 10))
        
        counts = df['sentiment'].value_counts()
        fig1 = Figure(figsize=(5, 3.5), dpi=100)
        ax1 = fig1.add_subplot(111)
        colors = {'positive': '#00cc00', 'negative': '#ff4444', 'neutral': '#4444ff'}
        bar_colors = [colors.get(sentiment, '#gray') for sentiment in counts.index]
        ax1.bar(counts.index, counts.values, color=bar_colors)
        ax1.set_title("Dataset Distribution")
        ax1.set_ylabel("Count")
        fig1.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, left_frame)
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right side - Input and results
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Stats
        stats_frame = tk.LabelFrame(right_frame, text="Model Stats", font=("Helvetica", 10, "bold"),
                                    bg="#f0f0f0", padx=10, pady=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        accuracy_text = tk.Label(stats_frame, text=f"Accuracy: {accuracy:.2%}", 
                                font=("Helvetica", 11, "bold"), bg="#f0f0f0")
        accuracy_text.pack(anchor=tk.W, pady=5)
        
        dataset_text = tk.Label(stats_frame, text=f"Total Posts: {len(df)}", 
                               font=("Helvetica", 11), bg="#f0f0f0")
        dataset_text.pack(anchor=tk.W, pady=5)
        
        # Input section
        input_frame = tk.LabelFrame(right_frame, text="Analyze Text", font=("Helvetica", 10, "bold"),
                                   bg="#f0f0f0", padx=10, pady=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(input_frame, text="Enter text:", font=("Helvetica", 9), bg="#f0f0f0").pack(anchor=tk.W, pady=(0, 5))
        
        self.text_input = tk.Text(input_frame, height=8, width=40, font=("Helvetica", 10))
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X)
        
        analyze_btn = tk.Button(button_frame, text="Analyze", command=self.analyze_sentiment,
                               bg="#2c3e50", fg="white", font=("Helvetica", 10, "bold"),
                               padx=20, pady=5, cursor="hand2")
        analyze_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_input,
                             bg="#7f8c8d", fg="white", font=("Helvetica", 10),
                             padx=20, pady=5, cursor="hand2")
        clear_btn.pack(side=tk.LEFT)
        
        # Result section
        self.result_frame = tk.LabelFrame(right_frame, text="Result", font=("Helvetica", 10, "bold"),
                                         bg="#f0f0f0", padx=10, pady=10)
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_label = tk.Label(self.result_frame, text="Enter text and click Analyze",
                                    font=("Helvetica", 11), bg="#f0f0f0", fg="#7f8c8d")
        self.result_label.pack(anchor=tk.W, pady=10)
        
        self.result_canvas_frame = tk.Frame(self.result_frame, bg="#f0f0f0")
        self.result_canvas_frame.pack(fill=tk.BOTH, expand=True)
    
    def clear_input(self):
        self.text_input.delete(1.0, tk.END)
        self.result_label.config(text="Enter text and click Analyze", fg="#7f8c8d")
        for widget in self.result_canvas_frame.winfo_children():
            widget.destroy()
    
    def analyze_sentiment(self):
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text to analyze!")
            return
        
        # Analyze in thread to prevent UI freeze
        thread = threading.Thread(target=self._perform_analysis, args=(text,))
        thread.start()
    
    def _perform_analysis(self, text):
        text_vec = vectorizer.transform([text])
        result = model.predict(text_vec)[0]
        probabilities = model.predict_proba(text_vec)[0]
        
        sentiment_emoji = {'positive': '😊', 'negative': '😞', 'neutral': '😐'}
        emoji = sentiment_emoji.get(result, '')
        
        # Update result label
        self.result_label.config(text=f"Sentiment: {emoji} {result.upper()}", 
                                fg="#00cc00" if result == "positive" else "#ff4444" if result == "negative" else "#4444ff",
                                font=("Helvetica", 13, "bold"))
        
        # Clear previous chart
        for widget in self.result_canvas_frame.winfo_children():
            widget.destroy()
        
        # Create result chart
        labels = ['positive', 'negative', 'neutral']
        values = probabilities
        
        fig2 = Figure(figsize=(4.5, 2.5), dpi=100)
        ax2 = fig2.add_subplot(111)
        colors = ['#00cc00', '#ff4444', '#4444ff']
        bars = ax2.bar(labels, values, color=colors)
        ax2.set_ylabel("Confidence")
        ax2.set_ylim(0, 1)
        ax2.set_title("Confidence Breakdown")
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.1%}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        fig2.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, self.result_canvas_frame)
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
app = SentimentAnalysisApp(root)
root.mainloop()
