# Sentiment Analysis

A complete sentiment analysis application that trains a machine learning model on social media posts and provides a desktop GUI for live text classification.

## What it does

- loads and preprocesses text data from `social_media_posts_v2.csv`
- removes English stopwords using NLTK
- converts text to TF-IDF features with unigrams and bigrams
- trains a `MultinomialNB` sentiment classifier
- displays dataset statistics and model accuracy
- provides a Tkinter-based graphical interface for custom input

## Key features

- ✅ Preprocessing with stopword removal
- ✅ TF-IDF vectorization
- ✅ Naive Bayes sentiment classification
- ✅ Dataset distribution chart
- ✅ Confidence score visualization
- ✅ Native desktop GUI (Tkinter)

## Requirements

- Python 3.10 or newer
- `pandas`
- `scikit-learn`
- `nltk`
- `matplotlib`
- `pillow`

## Quick setup

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas scikit-learn nltk matplotlib pillow
python -c "import nltk; nltk.download('stopwords')"
```

> On Windows, use `python` instead of `python3`, and activate the environment with `\.venv\Scripts\activate`.

## Run the application

```bash
python senti.py
```

You should see a desktop window with:

- dataset sentiment distribution chart
- model accuracy and total post count
- a text input area for custom sentiment analysis
- a confidence breakdown chart after each prediction

## Example usage

1. Open `senti.py`.
2. Enter a sentence in the text box.
3. Click **Analyze**.
4. Read the predicted sentiment and confidence levels.

## Project files

- `senti.py` — main Python application with model training and GUI
- `social_media_posts_v2.csv` — training dataset
- `README.md` — project documentation

## How it works

1. `senti.py` reads the CSV dataset.
2. Text is cleaned and stopwords are removed.
3. TF-IDF features are created from the cleaned text.
4. The model is trained on the processed dataset.
5. The Tkinter UI allows users to analyze new sentences.

## Troubleshooting

### `ModuleNotFoundError: No module named 'pandas'`

Make sure dependencies are installed in the active virtual environment:

```bash
pip install pandas scikit-learn nltk matplotlib pillow
```

### `ImportError: cannot import name 'ImageTk' from 'PIL'`

Install or upgrade Pillow:

```bash
pip install --upgrade pillow
```

### NLTK stopwords missing

Run:

```bash
python -c "import nltk; nltk.download('stopwords')"
```

## Notes

- The GUI uses Matplotlib embedded in Tkinter for charts.
- The model currently uses a simple Naive Bayes classifier, which is fast and easy to run on small datasets.
- For better results, you can replace the dataset or add more preprocessing.
