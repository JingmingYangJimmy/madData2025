import requests
import urllib.parse
import json

# Your OMDB API key and base URL
API_KEY = "933364d0"
BASE_URL = "https://www.omdbapi.com/"

def get_movie_data(title):
    # URL-encode the title
    encoded_title = urllib.parse.quote_plus(title)
    url = f"{BASE_URL}?t={encoded_title}&plot=short&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # You can add error checking here if the API response has an "Error" field
        if data.get("Response") == "True":
            return data
        else:
            print(f"OMDB API error for title '{title}': {data.get('Error')}")
            return None
    else:
        print(f"Failed to fetch data for '{title}' with status code {response.status_code}")
        return None

def main():
    # Read unique movie titles from a file (one title per line)
    with open("/Users/arjun/Documents/GitHub/madData2025/backend/unique_titles.txt", "r", encoding="utf-8") as file:
        titles = [line.strip() for line in file if line.strip()]

    movie_data_list = []
    seen_ids = set()  # Keep track of imdbIDs that we've already added

    for title in titles:
        print(f"Fetching data for: {title}")
        data = get_movie_data(title)
        if data:
            # Check if we've seen this movie (by imdbID) before
            imdb_id = data.get("imdbID")
            if imdb_id and imdb_id not in seen_ids:
                movie_data_list.append(data)
                seen_ids.add(imdb_id)
            else:
                print(f"Skipping duplicate or invalid entry for: {title}")

    # Save the movie data to a JSON file
    with open("movies_data_short.json", "w", encoding="utf-8") as outfile:
        json.dump(movie_data_list, outfile, indent=2)
    
    print("Movie data saved to 'movies_data.json'.")

if __name__ == "__main__":
    main()
