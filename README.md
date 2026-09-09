# BuzzKill — Mood-Based Movie & TV Recommender

**Live demo: [buzzzzkill.vercel.app](https://buzzzzkill.vercel.app/)** *(best viewed in Chrome)*

Built for **MadData 2025**.

Most recommenders ask *what* you watched. BuzzKill asks *how you want to feel*. You set two
mood sliders — **Sad ↔ Happy** and **Tense ↔ Calm** — pick up to three genres and a release
year, and it ranks thousands of movies and TV series against that mood.

The mood scores aren't hand-labeled: every title's plot summary and genre are run through a
zero-shot classifier (`facebook/bart-large-mnli`) to place it on those same two axes.

---

## How it works

```
Frontend (React)          Backend (Express)              Ranking (Python)
sliders + genres  ──POST──▶ /api/store-values ──exec──▶ get_user_preference.py
                             writes data.json            builds feature matrix
   ranked results ◀── JSON ──── stdout ◀────────────────  X · user_vector → sort
```

1. **Data collection** — `backend/get_data_api.py` and `get_tv_data.py` pull plots, posters
   and metadata from the [OMDb API](https://www.omdbapi.com/); the scrapers
   (`name_scraper.py`, `tv_scraper.py`, `review_scrape.py`) gather the title lists.
2. **Emotion classification** — `backend/movie-classification/plot_classification.py` and
   `backend/series-classification/series_classification.py` score each title on
   `Sad-Happy` and `Tense-Calm` using zero-shot classification over its plot and genre.
   Results land in `EmotionalMovies.json` and the series equivalents.
3. **Ranking** — each title becomes a vector `[SadHappy, TenseCalm, ...one-hot genres]`.
   Your slider + genre choices become a vector of the same shape, and the ranking is a
   single matrix multiply: `X @ user_vector`, sorted descending.
4. **Display** — the top matches come back with posters and plots and render in a carousel.

---

## Running locally

**Prerequisites:** Node.js 18+, Python 3.10+

**1. Python dependencies**

```bash
pip install numpy pandas requests transformers torch flask
```

**2. Start the backend** (from `backend/`, runs on port 3000)

```bash
cd backend && npm install && node server.js
```

**3. Start the frontend** (in a second terminal, from `my-app-frontend/`, opens on port 3001)

```bash
cd my-app-frontend && npm install && npm start
```

Create React App will notice port 3000 is taken and offer to use another port — say yes.
The frontend posts to `http://localhost:3000/api/store-values`, so the backend must be
running first or the "Confirm" button will fail.

> **Note:** `transformers` and `torch` are only needed if you re-run the classification
> scripts. The pre-computed emotion scores are already committed, so the app runs without them.

---

## Project layout

```
madData2025/
├── my-app-frontend/          React app (sliders, genre picker, results carousel)
│   └── src/App.js            main UI and the POST to the backend
├── backend/
│   ├── server.js             Express API; shells out to the ranking script
│   ├── get_user_preference.py   builds the feature matrix and ranks titles
│   ├── get_data_api.py       OMDb fetch for movies
│   ├── get_tv_data.py        OMDb fetch for series
│   ├── *_scraper.py          title-list and review scrapers
│   ├── movie-classification/ zero-shot emotion scoring for movies
│   └── series-classification/ zero-shot emotion scoring for series
├── EmotionalMovies.json      movies with Sad-Happy / Tense-Calm scores
├── EmotionalDamageSeries.json, EmotionalUnrecoverySeries.json   same, for series
└── app.py                    small Flask prototype of the ranking endpoint (unused)
```

## API

**`POST /api/store-values`**

```json
{
  "barValues": {
    "happy_index": 0.5,
    "calm_index": 0.6,
    "time_index": 2010,
    "genre": ["Drama", "Comedy"]
  }
}
```

`happy_index` and `calm_index` run from -1 to 1 in steps of 0.1, `time_index` from 1920 to
2025, and `genre` accepts up to three entries.
Responds with `{ message, storedData, rankedMovies }`, where `rankedMovies` is the top 100
titles with `Title`, `Poster`, `imdbID`, `Year` and `Plot`.

## Known limitations

- `get_user_preference.py` currently loads `EmotionalMovies.json` for both the movie and
  series data frames, so series rankings mirror movie rankings.
- `time_index` is collected from the UI but not yet used in the ranking.
- Preferences are appended to `backend/data.json` (gitignored) rather than a real database;
  only the most recent entry is used.
- The OMDb API key in `get_data_api.py` is hard-coded — move it to an environment variable
  before deploying anything.
