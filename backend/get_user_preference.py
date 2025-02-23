import json
import numpy as np
import pandas as pd


def load_jsonl(filepath):
    with open(filepath, 'r') as file:
        # Use json.loads() for JSONL format
        return [json.loads(line) for line in file]


def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)  # Use json.load() for normal JSON format


def calculate_score(movie, user_ratings):  # not currently implemented, see below
    return (
        abs(movie["AggregatedEmotion"]["Sad-Happy"] - user_ratings["happy_index"]) +
        abs(movie["AggregatedEmotion"]
            ["Tense-Calm"] - user_ratings["calm_index"])
    )


if __name__ == "__main__":
    # LOAD MOVIE AND SERIES DATA WITH EMOTIONAL RATINGS
    df_m = pd.read_json(
        "../EmotionalMovies.json")[["Title", "Genre", "AggregatedEmotion"]]
    df_s = pd.read_json(
        "../EmotionalMovies.json")[["Title", "Genre", "AggregatedEmotion"]]

    # Generated list of genres for movies
    lstm = []
    for gm in df_m["Genre"]:
        for g in gm.split(", "):
            if g not in lstm:
                lstm.append(g)
    # Generated list of genres for series
    lsts = []
    for gs in df_s["Genre"]:
        for g in gs.split(", "):
            if g not in lsts:
                lsts.append(g)

    # Change movie data with emotional ratings to desired format
    df_m["SadHappy"] = df_m["AggregatedEmotion"].apply(
        lambda x: x["Sad-Happy"])
    df_m["TenseCalm"] = df_m["AggregatedEmotion"].apply(
        lambda x: x["Tense-Calm"])
    df_m['genre_indices'] = df_m['Genre'].apply(
        lambda x: [lstm.index(g) for g in x.split(", ") if g in lstm])
    df_m['genre_row'] = df_m['genre_indices'].apply(
        lambda x: [1 if i in x else 0 for i in range(len(lstm))])
    df_m["matrixrow"] = df_m.apply(
        lambda row: [row["SadHappy"], row["TenseCalm"]] + row["genre_row"], axis=1)
    df_m[["Title", "matrixrow"]]
    X_m = np.array(df_m["matrixrow"].tolist())

    # Change series data with emotional ratings to desired format
    df_s["SadHappy"] = df_s["AggregatedEmotion"].apply(
        lambda x: x["Sad-Happy"])
    df_s["TenseCalm"] = df_s["AggregatedEmotion"].apply(
        lambda x: x["Tense-Calm"])
    df_s['genre_indices'] = df_s['Genre'].apply(
        lambda x: [lsts.index(g) for g in x.split(", ") if g in lsts])
    df_s['genre_row'] = df_s['genre_indices'].apply(
        lambda x: [1 if i in x else 0 for i in range(len(lsts))])
    df_s["matrixrow"] = df_s.apply(
        lambda row: [row["SadHappy"], row["TenseCalm"]] + row["genre_row"], axis=1)
    df_s[["Title", "matrixrow"]]
    X_s = np.array(df_s["matrixrow"].tolist())

    # LOAD USER DATA
    backend_data = load_json('data.json')  # Normal JSON for backend data

    # Extract the latest barValues from backend data
    latest_bar_values = backend_data[-1]["barValues"]

    # GENRE
    genre_indices = [lsts.index(g)
                     for g in latest_bar_values['genre'] if g in lsts]
    genre_row = [1 if i in genre_indices else 0 for i in range(len(lsts))]
    user_ratings = np.array([latest_bar_values['happy_index'],
                             latest_bar_values['calm_index']] + genre_row)

    # Get rankings based on user_ratings for movies and series
    array_m = X_m@user_ratings
    array_s = X_s@user_ratings

    res_df_m = pd.DataFrame(array_m, columns=["Value"])
    res_df_m["Title"] = df_m["Title"]
    res_df_m_sorted = res_df_m.sort_values(by="Value", ascending=False)

    res_df_s = pd.DataFrame(array_s, columns=["Value"])
    res_df_s["Title"] = df_s["Title"]
    res_df_s_sorted = res_df_s.sort_values(by="Value", ascending=False)

    # LOAD ALLL MOVIES DATA FROM movies_data.json and ALL SERIES DATA FROM tv_series_data.json
    movies_data = load_json("movies_data.json")
    movies_df = pd.DataFrame(movies_data)
    series_data = load_json("tv_series_data.json")
    series_df = pd.DataFrame(series_data)

    # Merge by title and output to frontend
    merged_df_m = res_df_s_sorted.merge(movies_df, on="Title", how="left")
    merged_df_s = res_df_m_sorted.merge(series_df, on="Title", how="left")
    desired_columns = ["Title", "Poster", "imdbID", "Year", "Plot"]
    filtered_df_m = merged_df_m[desired_columns]
    filtered_df_s = merged_df_s[desired_columns]
    merged_filtered_df = pd.concat(
        [filtered_df_m, filtered_df_s], ignore_index=True)
    print(merged_filtered_df.head(100).to_json(orient="records", indent=4))
