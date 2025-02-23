import json


def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def calculate_score(movie, user_ratings):
    return (
        abs(movie["EmotionalRatings"]["Sad_to_Happy"] - user_ratings["happy_index"]) +
        abs(movie["EmotionalRatings"]["Anxious_to_Calm"] -
            user_ratings["calm_index"])
    )


if __name__ == "__main__":
    # Load movies data and user data
    try:
        movies_data = load_json('../results_emotional_ratings.json')
    except json.decoder.JSONDecodeError:
        pass
        # def fix_json_file(input_filename, output_filename):
        #     with open(input_filename, 'r', encoding='utf-8') as file:
        #         content = file.read()

        #     # Fix formatting issues by wrapping in a list and separating objects properly
        #     fixed_content = '[{}]'.format(content.replace('}\n{', '},\n{'))

        #     try:
        #         json_data = json.loads(fixed_content)  # Ensure it's valid JSON
        #         with open(output_filename, 'w', encoding='utf-8') as output_file:
        #             json.dump(json_data, output_file, indent=4, ensure_ascii=False)
        #         print(f"Fixed JSON has been saved to {output_filename}")
        #     except json.JSONDecodeError as e:
        #         print(f"Error fixing JSON: {e}")

        #     # Fix emotional ratings file
        #     fix_json_file('../results_emotional_ratings.json',
        #                   '../results_emotional_ratings.json')
        movies_data = load_json('../results_emotional_ratings.json')
    backend_data = load_json('data.json')  # user data

    # Extract the latest barValues from backend data
    latest_bar_values = backend_data[-1]["barValues"]
    latest_bar_values

    user_ratings = {
        "happy_index": latest_bar_values["happy_index"],
        ##
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
            # Merges movie_data and all_movies_data
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
