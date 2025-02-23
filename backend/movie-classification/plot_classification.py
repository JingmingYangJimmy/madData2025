from transformers import pipeline
import json
import sys

print("Initializing zero-shot classifier...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def process_movie(movie):
    imdb_id = movie.get("imdbID")
    title = movie.get("Title")
    plot = movie.get("Plot")
    genre = movie.get("Genre")

    # Define emotion dimensions.
    dimensions = {
        "Sad-Happy": ("sad", "happy"),
        "Tense-Calm": ("tense", "calm")
    }
    aggregate = {dim: 0.0 for dim in dimensions.keys()}
    
    # Process each dimension in a batch call.
    for dim, (neg, pos) in dimensions.items():
        print(f"[{imdb_id}] Batch processing {dim} dimension for {title}...")
        results = classifier(,
            sequences=[plot, genre],
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
    
    result = {
        "Title": title,
        "imdbID": imdb_id,
        "AggregatedEmotion": aggregate
    }
    return result


if __name__ == "__main__":
    movies_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    print(f"Loading movies from {movies_filename}...")
    with open(movies_filename, "r", encoding="utf-8") as f:
        movies = json.load(f)
    
    total_movies = len(movies)
    print(f"Total movies in input: {total_movies}")

    for movie in movies[0:3]:
        movie["AggregatedEmotion"] = process_movie(movie)
    
    
    print("Done!")
