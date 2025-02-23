import requests
import urllib.parse
import json

API_KEY = "933364d0"
BASE_URL = "https://www.omdbapi.com/"

def get_tv_series_data(title):
    # URL-encode the title
    encoded_title = urllib.parse.quote_plus(title)
    # Add type=series to ensure we get TV series data
    url = f"{BASE_URL}?t={encoded_title}&type=series&plot=full&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data
        else:
            print(f"OMDB API error for title '{title}': {data.get('Error')}")
            return None
    else:
        print(f"Failed to fetch data for '{title}' with status code {response.status_code}")
        return None

def main():
    # Read unique TV series titles from file
    with open("unique_tv_series_titles.txt", "r", encoding="utf-8") as file:
        titles = [line.strip() for line in file if line.strip()]

    tv_data_list = []
    seen_ids = set()

    for title in titles:
       # print(f"Fetching data for TV series: {title}")
        data = get_tv_series_data(title)
        if data:
            imdb_id = data.get("imdbID")
            if imdb_id and imdb_id not in seen_ids:
                tv_data_list.append(data)
                seen_ids.add(imdb_id)
            else:
                print(f"Skipping duplicate or invalid entry for: {title}")

    with open("tv_series_data.json", "w", encoding="utf-8") as outfile:
        json.dump(tv_data_list, outfile, indent=2)
    print("TV series data saved to 'tv_series_data.json'.")

if __name__ == "__main__":
    main()
