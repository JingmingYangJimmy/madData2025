import json
from collections import defaultdict

# Define emotion keywords
emotion_keywords = {
    "Sad_to_Happy": ["love", "friendship", "hope", "happy", "inspire", "joy", "triumph"],
    "Fear_to_Anger": ["war", "battle", "revenge", "crime", "murder", "violence", "hostage"],
    "Anxious_to_Calm": ["thriller", "mystery", "trapped", "disaster", "danger", "rescue"]
}

# Function to rate emotional impact
def rate_emotions(genre, plot):
    ratings = defaultdict(float)
    
    # Check for keywords in genre and plot
    for emotion, keywords in emotion_keywords.items():
        count = sum(plot.lower().count(word) for word in keywords)
        count += sum(genre.lower().count(word) for word in keywords)
        ratings[emotion] = round(count / 5, 2)  # Normalize to a scale
    
    return dict(ratings)

# Load the movie data
file_path = "C:/Users/bazzi/Desktop/maddata/madData2025/backend/movies_data.json"
with open(file_path, "r", encoding="utf-8") as f:
    movies = json.load(f)

# Process movies
movies_with_emotions = []
for movie in movies:
    emotion_ratings = rate_emotions(movie["Genre"], movie["Plot"])
    movie_data = {
        "Title": movie["Title"],
        "EmotionalRatings": emotion_ratings
    }
    movies_with_emotions.append(movie_data)

# Save results
output_path = "c:/Users/bazzi/Desktop/maddata/madData2025/backend/movies_with_emotional_ratings.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(movies_with_emotions, f, indent=4)

print(f"Emotional ratings saved to {output_path}")
