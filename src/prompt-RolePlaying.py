import os
import pandas as pd
import csv

BASE_PATH = os.path.join("..", "data", "hetrec2011-movielens-2k-v2") + os.sep
OUTPUT_DIR = "prompt-RP"

def load_metadata(base_path):
    movie_tags = pd.read_csv(base_path + "movie_tags.dat", sep="\t", header=None,
                             names=["userId", "movieId", "tagid", "timestamp"],
                             quoting=csv.QUOTE_NONE, encoding="latin1")
    tags = pd.read_csv(base_path + "tags.dat", sep="\t", header=None,
                       names=["id", "value"],
                       quoting=csv.QUOTE_NONE, encoding="latin1")

    movie_tags['movieId'] = pd.to_numeric(movie_tags['movieId'], errors='coerce')
    movie_tags.dropna(subset=['movieId'], inplace=True)
    movie_tags['movieId'] = movie_tags['movieId'].astype(int)

    movie_tags['tagid'] = pd.to_numeric(movie_tags['tagid'], errors='coerce')
    movie_tags.dropna(subset=['tagid'], inplace=True)
    movie_tags['tagid'] = movie_tags['tagid'].astype(int)

    tags['id'] = pd.to_numeric(tags['id'], errors='coerce')
    tags.dropna(subset=['id'], inplace=True)
    tags['id'] = tags['id'].astype(int)

    movie_tags = movie_tags.merge(tags, left_on='tagid', right_on='id', how='left')

    return movie_tags

def load_movie_titles(base_path):
    movies = pd.read_csv(base_path + "movies.dat", sep="\t", encoding="latin1", usecols=['id', 'title'])
    movies.rename(columns={'id': 'movieId'}, inplace=True)
    movies['movieId'] = pd.to_numeric(movies['movieId'], errors='coerce')
    movies.dropna(subset=['movieId'], inplace=True)
    movies['movieId'] = movies['movieId'].astype(int)
    return movies

def main():
    movie_tags = load_metadata(BASE_PATH)
    movies = load_movie_titles(BASE_PATH)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    user_data = {}
    with open(BASE_PATH + "user_ratedmovies-timestamps.dat", 'r', encoding='latin1') as f:
        header = f.readline().strip().split('\t')
        for line in f:
            parts = line.strip().split('\t')
            row = dict(zip(header, parts))
            userId = int(row['userID'])
            rating = float(row['rating'])
            movieId = int(row['movieID'])

            if rating > 4:
                if userId not in user_data:
                    user_data[userId] = []
                user_data[userId].append(movieId)

    for userId, user_ratings in user_data.items():
        user_tags = set()
        for m in user_ratings:
            user_tags.update(movie_tags[movie_tags['movieId'] == m]['value'].dropna().tolist())

        rated_titles = movies[movies['movieId'].isin(user_ratings)]['title'].tolist()

        prompt = (
            "Given a user, as a Recommender System, please provide only the\n"
            "names of the top 50 recommendations. You know that the user likes\n"
            f"the following items: {', '.join(rated_titles)}.\n\n"
            f"Associated tags: {', '.join(sorted(user_tags))}"
        )

        output_file = os.path.join(OUTPUT_DIR, f"user_{userId}_gusti.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prompt)

        print(f"Prompt gusti utente {userId} salvato in {output_file}")

if __name__ == "__main__":
    main()
