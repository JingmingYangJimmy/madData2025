import json
import re
from collections import Counter

# Define common stopwords
stop_words = set([
    "the", "and", "to", "a", "of", "in", "is", "it", "that", "with", "as", "for", "on", "this",
    "an", "by", "be", "has", "at", "from", "about", "not", "have", "but", "if", "or", "he", "she",
    "they", "his", "her", "their", "which", "who", "what", "when", "where", "how", "why", "you",
    "we", "us", "them", "can", "will", "would", "should", "could", "so", "there", "been", "are",
    "being", "was", "were", "one", "all", "some", "any", "no", "just", "like", "more", "most",
    "other", "such", "into", "than", "out", "over", "up", "down", "left", "right", "through",
    "because", "while", "before", "after", "again", "same", "new", "old", "only", "even", "off",
    "own", "those", "these", "each", "both", "another", "many", "few", "every", "very", "much",
    "without", "against", "within", "among", "between","him","life","world","now","man","time","find","must",
    "two","get","family","help","young","its","however","years","back","father","way","himself","finds",
    "friends","take","story","named","do","first","team","soon","friend","home","also","lives",
    "wife","city","make","day","son","work","john","together","go","becomes","school","people",
    "woman","may","wants","takes","become","save","three","begins","hes","police","best","mother","past",
    "earth","gets","job","former","once","goes","men","decides","year","group","daughter","then",
    "house","later","stop","last","agent","town","trying","called","known","under","end","dr","discovers",
    "set","until","night","during","girl", "man", "woman", "boy", "girl", "child", "children", "friend", "friends", "family", "father",
    "mother", "brother", "sister", "husband", "wife", "son", "daughter", "person", "people",
    "group", "team",  "life", "world", "day", "night", "time", "place", "city", "town",
    "country", "home", "house", "school", "work", "office", "police", "criminal", "case", "murder",
    "mystery",  "escape", "quest", "storyline", "journey", "discover", "found", "happen", "realize", "begin", "start", "end",
    "happens", "find", "tries", "decides", "needs", "wants", "becomes", "meets", "joins",    "said", "says", "told", "tells", "talk", "talking", "listen", "watch", "watching",
    "walk", "walking", "run", "running", "comes", "goes", "arrives", "leaves", "gets", "makes",
    "turns", "seems", "appears", "looks", "thinks", "believes", "feels", "knows", "understands",
    "asks", "replies", "answers","high","learns","along","things","does","long","true","york","little",
    "still","jack","going","living","come","well","having","meanwhile","had","forces","future","know",
    "never","powerful","turn","four","whose","human","relationship","order","sent","behind","around",
    "live","away","s","too","army","meet","try","doesnt","good","money","led","return","american","everything","including","despite",
    "plan","face","ever","something","since","parents","power","forced","michael","peter","real","race","james",
    "finally","black","film","able","married","leads","keep","use","days","bring","themselves","part","see","working",
    "next","game","island","protect","movie","upon","white","control","join","crew","government","captain",
    "beautiful","based","five","lost","works","local","want","force","accross","planet","truth","bond",
    "car","sees","party","cant","los","accross","always","eventually","survive","others","angeles","girlfriend",
    "train","company","herself","decide","book","worlds","falls","land","land","max","action","boss","ben",
    "small","quickly","harry","someone","travel","chance","change","dark","great","officer","cia","might"
    "returns","following","yet","plans","business","lead","powers","frank","taking",
])

def get_word_frequencies(json_file, top_n=10):
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as file:
        movies = json.load(file)

    # Combine all plot descriptions into one text
    all_plots = " ".join(movie["Plot"] for movie in movies if "Plot" in movie)

    # Convert to lowercase and remove special characters
    all_plots_cleaned = re.sub(r"[^a-zA-Z\s]", "", all_plots.lower())

    # Tokenize the text
    tokens = all_plots_cleaned.split()

    # Remove stopwords
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Count word frequencies
    word_counts = Counter(filtered_tokens)

    # Get the most common words
    most_common_words = word_counts.most_common(top_n)

    return most_common_words

# Example usage
if __name__ == "__main__":
    json_file = "C:/Users/bazzi/Desktop/maddata/madData2025/backend/movies_data.json"
 # Replace with your JSON file path
    top_words = get_word_frequencies(json_file, top_n=40)
    print("Most common words in movie plots:")
    for word, count in top_words:
        print(f"{word}: {count}")
