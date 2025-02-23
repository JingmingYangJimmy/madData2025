from transformers import pipeline
import json
import sys

#print("Initializing zero-shot classifier...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def process_movie(movie):
    imdb_id = movie.get("imdbID")
    title = movie.get("Title")
    plot = movie.get("Plot")
    genre = movie.get("Genre")

    sequence_list = [plot, genre]

    # Define emotion dimensions.
    dimensions = {
        "Sad-Happy": ("sad", "happy"),
        "Tense-Calm": ("tense", "calm")
    }
    aggregate = {dim: 0.0 for dim in dimensions.keys()}
    
    # Process each dimension in a batch call.
    for dim, (neg, pos) in dimensions.items():
        #print(f"[{imdb_id}] Batch processing {dim} dimension for {title}...")
        results = classifier(
            sequences= sequence_list,
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
        aggregate[dim] = diff_sum / len(sequence_list)
    
    result = {
        "Title": title,
        "Year": movie.get("Year"),
        "Rated": movie.get("Rated"),
        "Released": movie.get("Released"),
        "Runtime": movie.get("Runtime"),
        "Genre": genre,
        "Director": movie.get("Director"),
        "Writer": movie.get("Writer"),
        "Actors": movie.get("Actors"),
        "Plot": plot,
        "Language": movie.get("Language"),
        "Country": movie.get("Country"),
        "Awards": movie.get("Awards"),
        "Poster": movie.get("Poster"),
        "Ratings": movie.get("Ratings"),
        "Metascore": movie.get("Metascore"),
        "imdbRating": movie.get("imdbRating"),
        "imdbVotes": movie.get("imdbVotes"),
        "imdbID": imdb_id,
        "Type": movie.get("Type"),
        "DVD": movie.get("DVD"),
        "BoxOffice": movie.get("BoxOffice"),
        "Production": movie.get("Production"),
        "Website": movie.get("Website"),
        "AggregatedEmotion": aggregate, 
        "Response": movie.get("Response"),
    }
    return result


if __name__ == "__main__":
    movies_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    #print(f"Loading movies from {movies_filename}...")
    with open(movies_filename, "r", encoding="utf-8") as f:
        movies = json.load(f)
    
    total_movies = len(movies)
    #print(f"Total movies in input: {total_movies}")
    i=0
    length = len(movies)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("[\n")
        for movie in movies:
            result = process_movie(movie)
            i+=1
            if i != length:
                f.write(json.dumps(result, ensure_ascii=False) + ",\n")
            else:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
        f.write("]\n")
        
    
    #print("Done!")