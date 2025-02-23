import numpy as np
import pandas as pd
import requests
import nltk
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def get_movie_reviews(imdb_id, num_reviews=5):
    """Fetches the first few user reviews from IMDb."""
    url = f"https://www.imdb.com/title/{imdb_id}/reviews"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = []
    
    for review in soup.find_all('div', class_='text show-more__control')[:num_reviews]:
        reviews.append(review.get_text())
    
    return reviews if reviews else ["No reviews available"]

def analyze_sentiment(reviews):
    """Performs sentiment analysis using NLTK and returns emotional ratings."""
    sentiment_scores = [sia.polarity_scores(review)['compound'] for review in reviews]
    avg_sentiment = np.mean(sentiment_scores)
    
    emotional_ratings = {
        "Sad_to_Happy": np.clip(avg_sentiment, -1, 1),
        "Fear_to_Anger": np.clip(-avg_sentiment, -1, 1),
        "Anxious_to_Calm": np.clip(avg_sentiment * 0.5, -1, 1)
    }
    return emotional_ratings

# Example movie dataset
movies_df = pd.DataFrame({
    "Title": ["Matrix", "Titanic", "John Wick"],
    "imdbID": ["tt0133093", "tt0120338", "tt2911666"]
})

# Apply sentiment-based rating
movies_df["Reviews"] = movies_df["imdbID"].apply(get_movie_reviews)
movies_df["EmotionalRatings"] = movies_df["Reviews"].apply(analyze_sentiment)

