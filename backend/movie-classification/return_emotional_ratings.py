import requests
import json
import re

# Few shot prompt to get emotional ratings for omdb responses


def get_emotional_ratings(api_key, OMDb_response):

    # Replace with your actual API key
    api_key = api_key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": """Instructions:
    I am building a movie recommender system based on emotions. 
    Complete the AI's message for the second movie with JSON format, 
    3 scales (Sad_to_Happy, Fear_to_Anger, Anxious_to_Calm), -1 to 1. 
    Include a "Reasoning" field explaining your emotional rating choices.
    ---
    Here are some examples.
    User: 
    {
        "Title": "The Secret Life of Walter Mitty",
        "Year": "2013",
        "Rated":"PG",
        "Released":"25 Dec 2013",
        "Runtime":"114 min",
        "Genre":"Adventure, Comedy, Drama",
        "Director":"Ben Stiller",
        "Writer":"Steve Conrad, James Thurber",
        "Actors":"Ben Stiller, Kristen Wiig, Jon Daly",
        "Plot":"When both he and a colleague are about to lose their job, Walter takes action by embarking on an adventure more extraordinary than anything he ever imagined.","Language":"English, Spanish, Icelandic","Country":"United States, United Kingdom","Awards":"5 wins & 18 nominations total",
        "Poster":"https://m.media-amazon.com/images/M/MV5BODYwNDYxNDk1Nl5BMl5BanBnXkFtZTgwOTAwMTk2MDE@._V1_SX300.jpg",
        "Ratings":[{"Source":"Internet Movie Database","Value":"7.3/10"},{"Source":"Rotten Tomatoes","Value":"52%"},{"Source":"Metacritic","Value":"54/100"}],
        "Metascore":"54",
        "imdbRating":"7.3",
        "imdbVotes":"351,568",
        "imdbID":"tt0359950",
        "Type":"movie",
        "DVD":"N/A",
        "BoxOffice":"$58,236,838",
        "Production":"N/A",
        "Website":"N/A",
        "Response":"True"
    } 
    AI: {
        "Title": "The Secret Life of Walter Mitty",
        "EmotionalRatings": {
            "Sad_to_Happy": 0.6,
            "Fear_to_Anger": -0.3,
            "Anxious_to_Calm": 0.5
        },
        "Reasoning": "The film has a strong uplifting and adventurous tone, emphasizing personal growth and fulfillment, hence a higher 'Sad_to_Happy' score. While there are moments of professional stress and some minor dangers, the film avoids intense fear or anger. The overall journey is one of self-discovery and finding peace, leading to a significant calming effect."
    }
    User: 
    {
        "Title":"Matrix",
        "Year":"1993",
        "Rated":"N/A",
        "Released":"01 Mar 1993",
        "Runtime":"60 min",
        "Genre":"Action, Drama, Fantasy",
        "Director":"N/A",
        "Writer":"Grenville Case",
        "Actors":"Nick Mancuso, Phillip Jarrett, Carrie-Anne Moss",
        "Plot":"Hitman Steven Matrix is shot, experiences afterlife, gets second chance by helping others. Wakes up, meets guides assigning cases where he aids people using unorthodox methods from past profession.",
        "Language":"English",
        "Country":"Canada",
        "Awards":"1 win total",
        "Poster":"https://m.media-amazon.com/images/M/MV5BM2JiZjU1NmQtNjg1Ni00NjA3LTk2MjMtNjYxMTgxODY0NjRhXkEyXkFqcGc@._V1_SX300.jpg",
        "Ratings":[{"Source":"Internet Movie Database","Value":"7.2/10"}],
        "Metascore":"N/A",
        "imdbRating":"7.2",
        "imdbVotes":"215",
        "imdbID":"tt0106062",
        "Type":"series",
        "totalSeasons":"N/A",
        "Response":"True"
    }
    AI:
    { 
        "Title": "Matrix", 
        "EmotionalRatings": 
        { 
            "Sad_to_Happy": 0.2, 
            "Fear_to_Anger": -0.1, 
            "Anxious_to_Calm": -0.4 
        },
        "Reasoning": "While the character is given a second chance, the premise of a hitman dealing with the consequences of his actions and being tasked with dangerous assignments creates a sense of tension and underlying sadness. There's a minimal presence of anger, but the overall tone is steeped in anxiety and unease, as the character navigates a morally ambiguous world. The 'Anxious_to_Calm' rating is lowered to reflect this constant state of tension."
    }""" + str(OMDb_response) + """
    AI:
    """
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_text = response.json(
        )["candidates"][0]["content"]["parts"][0]["text"]

        # Remove markdown code block and extract JSON
        json_string = re.search(r"```json\n(.*)\n```",
                                response_text, re.DOTALL).group(1)

        try:
            json_data = json.loads(json_string)
            print(json.dumps(json_data, indent=4))
        except json.JSONDecodeError:
            print("Error: Could not decode JSON from response.")
            print("Raw response text:", response_text)

    else:
        print(f"Error: {response.status_code}, {response.text}")


if __name__ == "__main__":
    import sys
    api_key = sys.argv[1]
    OMDb_file = sys.argv[2]
    with open(OMDb_file, 'r') as file:
        movies_data = json.load(file)
        for movie in movies_data[0:10]:
            get_emotional_ratings(api_key, movie_jsons)
