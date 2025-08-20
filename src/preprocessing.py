import pandas as pd
import os
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = "data/hetrec2011-movielens-2k-v2/user_ratedmovies-timestamps.dat"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE_FILTERED = "ratings_10core.tsv"
OUTPUT_FILE_TRAIN = "train.tsv"
OUTPUT_FILE_TEST = "test.tsv"


def strip_whitespace(df):
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df


def filter_k_core(df, k=10):
    while True:
        utenti_prima = df["userID"].nunique()
        film_prima = df["movieID"].nunique()

        user_counts = df["userID"].value_counts()
        df = df[df["userID"].isin(user_counts[user_counts >= k].index)]

        item_counts = df["movieID"].value_counts()
        df = df[df["movieID"].isin(item_counts[item_counts >= k].index)]

        utenti_dopo = df["userID"].nunique()
        film_dopo = df["movieID"].nunique()

        if utenti_prima == utenti_dopo and film_prima == film_dopo:
            break
    return df


def train_test_interaction_split(df, test_size=0.2, random_state=42):
    # Shuffle
    df = df.sample(frac=1, random_state=random_state).reset_index(drop=True)

    # Split per interazioni
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)

    # Filtra il test: utenti e item devono essere presenti nel train
    valid_users = set(train_df["userID"].unique())
    valid_items = set(train_df["movieID"].unique())

    test_df = test_df[
        test_df["userID"].isin(valid_users) &
        test_df["movieID"].isin(valid_items)
    ]

    return train_df, test_df


def clean_numeric_columns(df, columns):
    for col in columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=columns)
    return df


def enforce_numeric_and_clean(df):
    df["userId"] = pd.to_numeric(df["userId"], errors="coerce")
    df["movieId"] = pd.to_numeric(df["movieId"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["userId", "movieId", "rating", "timestamp"])
    df["userId"] = df["userId"].astype(int)
    df["movieId"] = df["movieId"].astype(int)
    df["rating"] = df["rating"].astype(float)
    df["timestamp"] = df["timestamp"].astype(int)
    return df


def main():
    print("Caricamento dati da file...")
    ratings = pd.read_csv(RAW_DATA_PATH, sep="\t", header=0, low_memory=False)

    ratings = strip_whitespace(ratings)

    ratings = ratings[['userID', 'movieID', 'rating', 'timestamp']]

    print("Pulizia e conversione colonne ID, rating e timestamp...")
    ratings = clean_numeric_columns(ratings, ["userID", "movieID", "rating", "timestamp"])

    ratings["userID"] = ratings["userID"].astype(int)
    ratings["movieID"] = ratings["movieID"].astype(int)
    ratings["rating"] = ratings["rating"].astype(float)
    ratings["timestamp"] = ratings["timestamp"].astype(int)

    print(f"Totale interazioni iniziali: {len(ratings)}")
    print(f"Utenti unici: {ratings['userID'].nunique()} | Film unici: {ratings['movieID'].nunique()}")

    ratings_filtrato = filter_k_core(ratings, k=10)

    print("\nDopo applicazione filtro 10-core:")
    print(f"Interazioni: {len(ratings_filtrato)}")
    print(f"Utenti unici: {ratings_filtrato['userID'].nunique()} | Film unici: {ratings_filtrato['movieID'].nunique()}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path_filtered = os.path.join(OUTPUT_DIR, OUTPUT_FILE_FILTERED)
    ratings_filtrato.to_csv(path_filtered, sep="\t", index=False)
    print(f"File filtro 10-core salvato in: {path_filtered}")

    # Split sulla base delle interazioni
    train_df, test_df = train_test_interaction_split(ratings_filtrato, test_size=0.2)

    train_df = train_df.rename(columns={"userID": "userId", "movieID": "movieId"})
    test_df = test_df.rename(columns={"userID": "userId", "movieID": "movieId"})

    train_df = enforce_numeric_and_clean(train_df)
    test_df = enforce_numeric_and_clean(test_df)

    path_train = os.path.join(OUTPUT_DIR, OUTPUT_FILE_TRAIN)
    path_test = os.path.join(OUTPUT_DIR, OUTPUT_FILE_TEST)

    train_df.to_csv(path_train, sep="\t", index=False)
    test_df.to_csv(path_test, sep="\t", index=False)

    print(f"Train set salvato in: {path_train} (utenti: {train_df['userId'].nunique()}, interazioni: {len(train_df)})")
    print(f"Test set salvato in: {path_test} (utenti: {test_df['userId'].nunique()}, interazioni: {len(test_df)})")


if __name__ == "__main__":
    main()
