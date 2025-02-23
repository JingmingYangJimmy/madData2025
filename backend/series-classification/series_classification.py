from transformers import pipeline
import json
import sys

#print("Initializing zero-shot classifier...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def process_series(series):
    imdb_id = series.get("imdbID")
    title = series.get("Title")
    plot = series.get("Plot")
    genre = series.get("Genre")

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
        "Year": series.get("Year"),
        "Rated": series.get("Rated"),
        "Released": series.get("Released"),
        "Runtime": series.get("Runtime"),
        "Genre": genre,
        "Director": series.get("Director"),
        "Writer": series.get("Writer"),
        "Actors": series.get("Actors"),
        "Plot": plot,
        "Language": series.get("Language"),
        "Country": series.get("Country"),
        "Awards": series.get("Awards"),
        "Poster": series.get("Poster"),
        "Ratings": series.get("Ratings"),
        "Metascore": series.get("Metascore"),
        "imdbRating": series.get("imdbRating"),
        "imdbVotes": series.get("imdbVotes"),
        "imdbID": imdb_id,
        "Type": series.get("Type"),
        "totalSeasons": series.get("totalSeasons"),
        "AggregatedEmotion": aggregate, 
        "Response": series.get("Response"),
    }
    return result


if __name__ == "__main__":
    series_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    #print(f"Loading series from {series_filename}...")
    with open(series_filename, "r", encoding="utf-8") as f:
        series_all = json.load(f)
    
    total_series = len(series_all)
    #print(f"Total series in input: {total_series}")
    i=0
    length = len(series_all)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("[\n")
        for series in series_all[3171:]:
            result = process_series(series)
            i+=1
            if i != length:
                f.write(json.dumps(result, ensure_ascii=False) + ",\n")
            else:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
        f.write("]\n")
        
    
    #print("Done!")