import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import time
import csv
import threading
from collections import Counter

# -------- LOADING PROCESS --------
def loading_process():
    print("Starting Sentiment Analyzer...")
    time.sleep(1)
    progress_var.set(25)
    root.update_idletasks()

    print("Loading resources...")
    nltk.download('vader_lexicon', quiet=True)
    time.sleep(1)
    progress_var.set(50)
    root.update_idletasks()

    print("Initializing model...")
    time.sleep(1)
    progress_var.set(75)
    root.update_idletasks()

    print("Ready!\n--------------------------")
    progress_var.set(100)
    root.update_idletasks()
    time.sleep(0.5)

    # Hide loading screen and show main UI
    loading_frame.pack_forget()
    main_frame.pack(fill=tk.BOTH, expand=True)

# -------- MODEL --------
sia = SentimentIntensityAnalyzer()

# Store user inputs
user_data = []
analysis_history = []

# -------- SENTIMENT FUNCTION --------
def get_sentiment(text):
    scores = sia.polarity_scores(text)
    compound = scores['compound']

    if compound > 0.05:
        sentiment = "Positive"
    elif compound < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, scores

# -------- FUNCTIONS --------
def analyze_input():
    user_text = text_input.get("1.0", tk.END).strip()

    if not user_text:
        messagebox.showwarning("Input Error", "Please enter some text")
        return

    sentiment, scores = get_sentiment(user_text)
    user_data.append(sentiment)

    # Update result
    result_label.config(text=f"Sentiment: {sentiment}")
    score_label.config(text=".3f")

    # Update stats
    update_stats()

    # Add to history
    history_list.insert(0, f"{sentiment}: {user_text[:50]}{'...' if len(user_text) > 50 else ''}")
    analysis_history.append((user_text, sentiment, scores))

    text_input.delete("1.0", tk.END)

def update_stats():
    if not user_data:
        stats_label.config(text="No analyses yet")
        return

    total = len(user_data)
    counts = Counter(user_data)
    pos_pct = (counts.get('Positive', 0) / total) * 100
    neg_pct = (counts.get('Negative', 0) / total) * 100
    neu_pct = (counts.get('Neutral', 0) / total) * 100

    stats_text = f"Total: {total} | Positive: {counts.get('Positive', 0)} ({pos_pct:.1f}%) | Negative: {counts.get('Negative', 0)} ({neg_pct:.1f}%) | Neutral: {counts.get('Neutral', 0)} ({neu_pct:.1f}%)"
    stats_label.config(text=stats_text)

def show_graph():
    if not user_data:
        messagebox.showwarning("No Data", "No inputs to show graph")
        return

    counts = Counter(user_data)

    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Bar chart
    sentiments = ['Positive', 'Negative', 'Neutral']
    values = [counts.get(sent, 0) for sent in sentiments]
    colors = ['#4CAF50', '#F44336', '#FFC107']
    ax1.bar(sentiments, values, color=colors)
    ax1.set_title("Sentiment Distribution (Bar Chart)")
    ax1.set_ylabel("Count")

    # Pie chart
    ax2.pie(values, labels=sentiments, colors=colors, autopct='%1.1f%%')
    ax2.set_title("Sentiment Distribution (Pie Chart)")

    plt.tight_layout()
    plt.show()

def clear_data():
    if messagebox.askyesno("Clear Data", "Are you sure you want to clear all data?"):
        user_data.clear()
        analysis_history.clear()
        history_list.delete(0, tk.END)
        result_label.config(text="")
        score_label.config(text="")
        update_stats()

def export_csv():
    if not analysis_history:
        messagebox.showwarning("No Data", "No data to export")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    if filename:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Text', 'Sentiment', 'Compound', 'Positive', 'Negative', 'Neutral'])

            for text, sentiment, scores in analysis_history:
                writer.writerow([
                    text,
                    sentiment,
                    scores['compound'],
                    scores['pos'],
                    scores['neg'],
                    scores['neu']
                ])

        messagebox.showinfo("Export Complete", f"Data exported to {filename}")

def batch_analyze_csv():
    filename = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    if not filename:
        return

    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            texts = []

            for row in reader:
                if 'text' in row:
                    texts.append(row['text'])
                elif len(row) == 1:  # Assume single column
                    texts.append(list(row.values())[0])

        if not texts:
            messagebox.showerror("Error", "No text column found in CSV")
            return

        # Analyze all texts
        results = []
        for text in texts:
            if text.strip():
                sentiment, scores = get_sentiment(text.strip())
                user_data.append(sentiment)
                analysis_history.append((text.strip(), sentiment, scores))
                results.append(f"{sentiment}: {text.strip()[:50]}{'...' if len(text.strip()) > 50 else ''}")

        # Update UI
        update_stats()
        for result in results[-10:]:  # Show last 10
            history_list.insert(0, result)

        messagebox.showinfo("Batch Analysis Complete", f"Analyzed {len(results)} texts")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process CSV: {str(e)}")

def real_time_analyze(event=None):
    text = text_input.get("1.0", tk.END).strip()
    if text:
        sentiment, scores = get_sentiment(text)
        real_time_label.config(text=f"Real-time: {sentiment} (.3f)")
    else:
        real_time_label.config(text="")

def show_about():
    messagebox.showinfo("About", "Sentiment Analysis App\n\nAnalyzes text sentiment using NLTK's VADER.\n\nFeatures:\n- Real-time analysis\n- Batch CSV processing\n- Export results\n- Visual graphs\n- Analysis history")

# -------- UI --------
root = tk.Tk()
root.title("Sentiment Analyzer")
root.geometry("850x650")
root.configure(bg='#f0f0f0')

# Create gradient background
def create_gradient(canvas, width, height, color1, color2):
    """Create a vertical gradient on the canvas"""
    for i in range(height):
        # Calculate color interpolation
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

        r = int(r1 + (r2 - r1) * i / height)
        g = int(g1 + (g2 - g1) * i / height)
        b = int(b1 + (b2 - b1) * i / height)

        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, width, i, fill=color)

# Loading screen
loading_frame = ttk.Frame(root)
loading_frame.pack(fill=tk.BOTH, expand=True)

# Gradient canvas for loading
loading_canvas = tk.Canvas(loading_frame, highlightthickness=0)
loading_canvas.pack(fill=tk.BOTH, expand=True)
create_gradient(loading_canvas, 800, 600, '#667eea', '#764ba2')

# Loading content on top of gradient
loading_content = ttk.Frame(loading_frame)
loading_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

ttk.Label(loading_content, text="Loading Sentiment Analyzer...", font=("Arial", 16, "bold"), background='#667eea', foreground='white').pack(pady=20)
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(loading_content, variable=progress_var, maximum=100, length=300)
progress_bar.pack(pady=20)

# Main UI
main_frame = ttk.Frame(root)

# Gradient background for main UI
main_canvas = tk.Canvas(main_frame, highlightthickness=0)
main_canvas.pack(fill=tk.BOTH, expand=True)
create_gradient(main_canvas, 800, 600, '#f093fb', '#f5576c')

# Content frame on top of gradient
content_frame = ttk.Frame(main_frame)
content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Title
title_frame = ttk.Frame(content_frame)
title_frame.pack(fill=tk.X, pady=10)
ttk.Label(title_frame, text="Advanced Sentiment Analysis", font=("Arial", 18, "bold"), background='#f093fb', foreground='white').pack()

# Input section
input_frame = ttk.LabelFrame(content_frame, text="Text Input", padding=10)
input_frame.pack(fill=tk.X, padx=10, pady=5)

text_input = scrolledtext.ScrolledText(input_frame, height=4, wrap=tk.WORD, font=("Arial", 10))
text_input.pack(fill=tk.X)
text_input.bind('<KeyRelease>', real_time_analyze)

real_time_label = ttk.Label(input_frame, text="", foreground="#333", font=("Arial", 9, "italic"))
real_time_label.pack(anchor=tk.W, pady=(5,0))

# Buttons
button_frame = ttk.Frame(content_frame)
button_frame.pack(fill=tk.X, padx=10, pady=5)

style = ttk.Style()
style.configure('Colorful.TButton', font=('Arial', 9, 'bold'))

analyze_btn = ttk.Button(button_frame, text="Analyze Text", command=analyze_input, style='Colorful.TButton')
analyze_btn.pack(side=tk.LEFT, padx=(0,5))

batch_btn = ttk.Button(button_frame, text="Batch Analyze CSV", command=batch_analyze_csv, style='Colorful.TButton')
batch_btn.pack(side=tk.LEFT, padx=(0,5))

graph_btn = ttk.Button(button_frame, text="Show Graphs", command=show_graph, style='Colorful.TButton')
graph_btn.pack(side=tk.LEFT, padx=(0,5))

export_btn = ttk.Button(button_frame, text="Export CSV", command=export_csv, style='Colorful.TButton')
export_btn.pack(side=tk.LEFT, padx=(0,5))

clear_btn = ttk.Button(button_frame, text="Clear Data", command=clear_data, style='Colorful.TButton')
clear_btn.pack(side=tk.LEFT, padx=(0,5))

about_btn = ttk.Button(button_frame, text="About", command=show_about, style='Colorful.TButton')
about_btn.pack(side=tk.RIGHT)

# Results section
results_frame = ttk.LabelFrame(content_frame, text="Results", padding=10)
results_frame.pack(fill=tk.X, padx=10, pady=5)

result_label = ttk.Label(results_frame, text="", font=("Arial", 12, "bold"), foreground="#2e7d32")
result_label.pack(anchor=tk.W)

score_label = ttk.Label(results_frame, text="", foreground="#666", font=("Arial", 9))
score_label.pack(anchor=tk.W)

stats_label = ttk.Label(results_frame, text="No analyses yet", foreground="#666", font=("Arial", 9))
stats_label.pack(anchor=tk.W, pady=(10,0))

# History section
history_frame = ttk.LabelFrame(content_frame, text="Analysis History", padding=10)
history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

history_list = tk.Listbox(history_frame, height=10, font=("Arial", 9), selectbackground="#f5576c")
history_list.pack(fill=tk.BOTH, expand=True)

# Start loading in background
loading_thread = threading.Thread(target=loading_process)
loading_thread.start()

root.mainloop()