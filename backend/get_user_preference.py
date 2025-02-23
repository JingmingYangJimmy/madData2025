import json


def load_jsonl(filepath):
    with open(filepath, 'r') as file:
        # Use json.loads() for JSONL format
        return [json.loads(line) for line in file]


def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)  # Use json.load() for normal JSON format


def calculate_score(movie, user_ratings):
    return (
        abs(movie["AggregatedEmotion"]["Sad-Happy"] - user_ratings["happy_index"]) +
        abs(movie["AggregatedEmotion"]
            ["Tense-Calm"] - user_ratings["calm_index"])
    )


if __name__ == "__main__":
    # Load movies data as JSONL and user data as normal JSON
    movies_data = load_jsonl('../movies_emotion_scores.jsonl')

    backend_data = load_json('data.json')  # Normal JSON for backend data

    # Extract the latest barValues from backend data
    latest_bar_values = backend_data[-1]["barValues"]

    user_ratings = {
        "happy_index": latest_bar_values["happy_index"],
        "calm_index": latest_bar_values["calm_index"]
    }

    # Rank the movies
    for movie in movies_data:
        movie["score"] = calculate_score(movie, user_ratings)

    # Load the data that has all the movie files
    all_movies_data = load_json('movies_data.json')

    merged_movies_data = []

    for movie in movies_data:
        # Find the matching movie from all_movies_data by Title
        matching_movie = next(
            (m for m in all_movies_data if m["Title"] == movie["Title"]), None)

        if matching_movie:
            # Merge data from both sources
            merged_movie = {**movie, **matching_movie}
            merged_movies_data.append(merged_movie)

    # Rank the merged movies by score
    ranked_movies = sorted(
        merged_movies_data, key=lambda x: x["score"], reverse=True)

    # Extract titles and posters into a new list
    ranked_movies_with_posters = [
        {"Title": movie["Title"], "Poster": movie["Poster"]} for movie in ranked_movies]

    # Output the result as JSON
    print(json.dumps(ranked_movies_with_posters, indent=4))
