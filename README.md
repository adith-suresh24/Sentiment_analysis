# 📊 Sentiment Analysis

## 📌 Project Overview

This project is a **Sentiment Analysis Application** designed to support individuals with **Autism Spectrum Disorder (ASD)** and others who may find it difficult to interpret emotional tone in text.

It analyzes user input and classifies it as **Positive, Negative, or Neutral**, helping improve understanding of social media interactions.

---

## 🎯 Purpose

* Assist users in understanding emotional tone in messages
* Improve social communication skills
* Reduce confusion in online interactions
* Provide clear and instant emotional interpretation

---

## 🌟 Use Cases / Importance

* Helps understand **emotional tone in text messages**
* Reduces **misinterpretation in conversations**
* Supports safer and more confident **social media usage**
* Identifies **harmful or toxic comments**
* Helps detect **bullying or negative language**
* Improves **emotional intelligence (EQ)**
* Encourages **positive online behavior**
* Supports users with **social communication difficulties**
* Useful for **AI/NLP learning projects**
* Promotes **inclusive technology development**

---

## 🚀 Features

* 🖥️ Simple Tkinter-based GUI
* 💬 Real-time sentiment analysis
* 📊 Bar graph visualization of user inputs
* ⚡ Lightweight and fast
* 🧠 Uses VADER Sentiment Analysis (NLTK)
* 📈 (Optional) Dataset-based sentiment distribution
* 🔍 Input-based sentiment prediction

---

## 🛠️ Technologies Used

* Python 3.10+
* Tkinter
* NLTK
* Matplotlib
* Pandas (optional dataset handling)

---

## 📂 Project Structure

```
project-folder/
│
├── main.py
├── social_media_posts_v2.csv   (optional)
├── README.md
```

---

## ⚙️ Requirements

* Python 3.10 or newer
* pandas
* nltk
* matplotlib

---

## ⚡ Quick Setup

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas nltk matplotlib
python -c "import nltk; nltk.download('vader_lexicon')"
```

> On Windows, use `python` instead of `python3`, and activate using:

```
.venv\Scripts\activate
```

---

## ▶️ Run the Application

```bash
python main.py
```

---

## 🧪 How It Works

### Current Version (VADER-based)

1. User enters text
2. NLTK VADER analyzes sentiment
3. Output is classified as:

   * Positive 😊
   * Negative 😞
   * Neutral 😐
4. Graph shows sentiment distribution of user inputs

---

### 🔬 (Optional Advanced Version - ML Based)

If extended using dataset:

1. CSV dataset is loaded
2. Text is cleaned and processed
3. Features are extracted (e.g., TF-IDF)
4. A machine learning model is trained
5. UI allows prediction on new inputs

---

## 📊 Example

**Input:**

```
I really love this app!
```

**Output:**

```
Sentiment: Positive
```

---

## ⚠️ Limitations

* Not a medical or diagnostic tool
* May not detect sarcasm accurately
* Works best with simple sentences
* Data is not saved after closing

---

## 🔮 Future Improvements

* Save user input history
* Add voice input support
* Real-time graph updates
* Train custom ML model (TF-IDF + sklearn)
* Add confidence scores
* Convert to web/mobile app
* Dark mode UI

---

## 🛠️ Troubleshooting

* If NLTK error occurs:

  ```
  import nltk
  nltk.download('vader_lexicon')
  ```
* Ensure all dependencies are installed
* Check Python version (3.10+)

---

## As For app.py

The app.py file is a standalone project that contains all the necessary functionality within a single file. It does not rely on any external CSV files by default, making it simple to run and easy to set up.

However, if you want to generate customized feedback or modify the results, you can integrate a CSV file from external sources as needed. Ensure that the CSV file follows the expected format and structure so that the application can read and process the data correctly.

To use a CSV file, place it in the project directory and update the file path in the code accordingly. You may also need to adjust the data parsing logic depending on the format of your CSV.

Before running the application, make sure all required dependencies are installed. Once everything is set up, you can execute the script normally, and it will either use the default logic or the customized data provided through the CSV file.


---

## 👨‍💻 Author

Adith Suresh

---

## 📄 Disclaimer

This tool is designed for assistance purposes only and should not replace professional guidance.
