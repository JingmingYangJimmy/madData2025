import json


def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def calculate_score(movie, user_ratings):
    return (
        abs(movie["EmotionalRatings"]["Sad_to_Happy"] - user_ratings["happy_index"]) +
        abs(movie["EmotionalRatings"]["Fear_to_Anger"] - user_ratings["fear_index"]) +
        abs(movie["EmotionalRatings"]["Anxious_to_Calm"] -
            user_ratings["anxious_index"])
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
        "fear_index": latest_bar_values["fear_index"],
        ##
        "anxious_index": latest_bar_values["anxious_index"]
    }

    # Rank the movies
    for movie in movies_data:
        movie["score"] = calculate_score(movie, user_ratings)

    ranked_movies = sorted(
        movies_data, key=lambda x: x["score"])

    # Print the ranked movie titles
    ranked_titles = [
        movie["Title"] for movie in ranked_movies]
    for idx, title in enumerate(ranked_titles, 1):
        print(f"{idx}. {title}")
