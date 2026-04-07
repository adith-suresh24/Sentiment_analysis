import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import time

# -------- LOADING PROCESS --------
print("Starting Sentiment Analyzer...")
time.sleep(1)

print("Loading resources...")
nltk.download('vader_lexicon')
time.sleep(1)

print("Initializing model...")
time.sleep(1)

print("Ready!\n--------------------------")

# -------- MODEL --------
sia = SentimentIntensityAnalyzer()

# Store user inputs
user_data = []

# -------- SENTIMENT FUNCTION --------
def get_sentiment(text):
    score = sia.polarity_scores(text)['compound']
    
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

# -------- FUNCTIONS --------
def analyze_input():
    user_text = entry.get()
    
    if user_text == "":
        messagebox.showwarning("Input Error", "Please enter some text")
        return
    
    sentiment = get_sentiment(user_text)
    user_data.append(sentiment)
    
    result_label.config(text="Sentiment: " + sentiment)
    entry.delete(0, tk.END)

def show_graph():
    if len(user_data) == 0:
        messagebox.showwarning("No Data", "No inputs to show graph")
        return
    
    counts = {
        "Positive": user_data.count("Positive"),
        "Negative": user_data.count("Negative"),
        "Neutral": user_data.count("Neutral")
    }
    
    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.title("User Input Sentiment Analysis")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.show()

# -------- UI --------
root = tk.Tk()
root.title("Sentiment Analyzer")
root.geometry("400x300")

title = tk.Label(root, text="Sentiment Analysis", font=("Arial", 16))
title.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

analyze_btn = tk.Button(root, text="Analyze Text", command=analyze_input)
analyze_btn.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

graph_btn = tk.Button(root, text="Show Graph", command=show_graph)
graph_btn.pack(pady=10)

root.mainloop()