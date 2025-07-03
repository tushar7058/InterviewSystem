import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon', quiet=True)

def analyze_text(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment

if __name__ == "__main__":
    sample = "This is a great interview."
    print(analyze_text(sample))
