import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import math
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_imdb_reviews(imdb_id, session):
    """
    Fetches reviews for the given IMDb ID from imdb.com using the provided session.
    """
    url = f"https://www.imdb.com/title/{imdb_id}/reviews/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/88.0.4324.150 Safari/537.36"
        )
    }
    print(f"[{imdb_id}] Fetching reviews from URL: {url}")
    try:
        response = session.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"[{imdb_id}] Exception during GET: {e}")
        return []
    
    if response.status_code != 200:
        print(f"[{imdb_id}] Failed to fetch page. Status code: {response.status_code}")
        return []
    
    print(f"[{imdb_id}] Successfully fetched reviews page.")
    soup = BeautifulSoup(response.text, "html.parser")
    review_containers = soup.find_all("div", class_="ipc-html-content-inner-div")
    print(f"[{imdb_id}] Found {len(review_containers)} potential review container(s).")
    
    reviews = []
    for container in review_containers:
        review_text = container.get_text(strip=True)
        if review_text:
            reviews.append(review_text)
    print(f"[{imdb_id}] Extracted {len(reviews)} reviews.")
    return reviews

print("Initializing zero-shot classifier...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def compute_year_metric(year_str, min_year=1920, max_year=2025):
    """
    Computes a year metric normalized from -1 (for min_year) to +1 (for max_year).
    If the movie's year falls outside this range, it is clamped.
    """
    try:
        year = int(year_str)
        if year < min_year:
            year = min_year
        elif year > max_year:
            year = max_year
        metric = (year - min_year) / (max_year - min_year) * 2 - 1
        return round(metric, 2)
    except Exception as e:
        print(f"Error computing year metric for year '{year_str}': {e}")
        return None

def process_movie(movie, session):
    """
    Given a movie dict (with at least "Title", "imdbID", and "Year"),
    fetch its reviews, compute averaged emotion scores (each metric in [-1, 1]),
    and return a result dictionary.
    """
    imdb_id = movie.get("imdbID")
    title = movie.get("Title")
    year_str = movie.get("Year")
    
    reviews = get_imdb_reviews(imdb_id, session)
    if not reviews:
        print(f"[{imdb_id}] No reviews found for {title}.")
        year_metric = compute_year_metric(year_str) if year_str else None
        return {
            "Title": title,
            "imdbID": imdb_id,
            "Year": year_str,
            "YearMetric": year_metric,
            "AggregatedEmotion": {}
        }
    
    # Define emotion dimensions.
    dimensions = {
        "Sad-Happy": ("sad", "happy"),
        "Tense-Calm": ("tense", "calm")
    }
    aggregate = {dim: 0.0 for dim in dimensions.keys()}
    
    # Process each dimension in a batch call.
    for dim, (neg, pos) in dimensions.items():
        print(f"[{imdb_id}] Batch processing {dim} dimension for {title}...")
        results = classifier(
            sequences=reviews,
            candidate_labels=[neg, pos],
            multi_label=False
        )
        if not isinstance(results, list):
            results = [results]
        diff_sum = 0.0
        for res in results:
            labels = res["labels"]
            scores = res["scores"]
            score_neg = scores[labels.index(neg)]
            score_pos = scores[labels.index(pos)]
            diff_sum += (score_pos - score_neg)
        aggregate[dim] = diff_sum / len(reviews)
    
    year_metric = compute_year_metric(year_str) if year_str else None
    result = {
        "Title": title,
        "imdbID": imdb_id,
        "Year": year_str,
        "YearMetric": year_metric,
        "AggregatedEmotion": aggregate
    }
    return result

def process_and_write_movie(movie, session, output_filename, lock):
    result = process_movie(movie, session)
    with lock:
        with open(output_filename, "a", encoding="utf-8") as out_file:
            out_file.write(json.dumps(result) + "\n")
            out_file.flush()
    print(f"Processed and wrote movie: {movie.get('Title')} ({movie.get('imdbID')})")

if __name__ == "__main__":
    movies_filename = r"/Users/arjun/Documents/GitHub/madData2025/backend/movies_data.json"
    output_filename = "movies_emotion_scores.json"
    
    print(f"Loading movies from {movies_filename}...")
    with open(movies_filename, "r", encoding="utf-8") as f:
        movies = json.load(f)
    
    # Read already processed IMDb IDs from the output file, if it exists.
    processed = set()
    if os.path.exists(output_filename):
        with open(output_filename, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    processed.add(data.get("imdbID"))
    
    total_movies = len(movies)
    print(f"Total movies in input: {total_movies}")
    
    lock = threading.Lock()
    session = requests.Session()
    max_workers = 4  # Adjust based on your system resources.
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for movie in movies:
            imdb_id = movie.get("imdbID")
            if imdb_id in processed:
                print(f"Skipping {movie.get('Title')} ({imdb_id}) as already processed.")
                continue
            futures.append(executor.submit(process_and_write_movie, movie, session, output_filename, lock))
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing a movie: {e}")
    
    print("Done!")
