import pandas as pd

BASE_PATH = "../data/hetrec2011-movielens-2k-v2/"

def load_dat(path, sep="\t", names=None):
    return pd.read_csv(path, sep=sep, names=names, encoding="latin1")

# -------------------
# Caricamento dati
# -------------------
movies = pd.read_csv(BASE_PATH + "movies.dat", sep="\t", encoding="latin1")
movies = movies.rename(columns={"id": "item_id"})
movies["year"] = movies["year"].fillna("").astype(str)

years = movies[["item_id", "year"]].rename(columns={"year": "attribute_value"})
years["attribute_name"] = "year"

actors = pd.read_csv(BASE_PATH + "movie_actors.dat", sep="\t", encoding="latin1")[["movieID", "actorName"]]
actors = actors.rename(columns={"movieID": "item_id", "actorName": "attribute_value"})
actors["attribute_name"] = "actor"

genres = pd.read_csv(BASE_PATH + "movie_genres.dat", sep="\t", encoding="latin1").rename(columns={"movieID": "item_id", "genre": "attribute_value"})
genres["attribute_name"] = "genre"

directors = pd.read_csv(BASE_PATH + "movie_directors.dat", sep="\t", encoding="latin1")[["movieID", "directorName"]]
directors = directors.rename(columns={"movieID": "item_id", "directorName": "attribute_value"})
directors["attribute_name"] = "director"

countries = pd.read_csv(BASE_PATH + "movie_countries.dat", sep="\t", encoding="latin1").rename(columns={"movieID": "item_id", "country": "attribute_value"})
countries["attribute_name"] = "country"

locations = pd.read_csv(BASE_PATH + "movie_locations.dat", sep="\t", encoding="latin1")[["movieID", "location1"]]
locations = locations.rename(columns={"movieID": "item_id", "location1": "attribute_value"})
locations["attribute_name"] = "location"

movie_tags = pd.read_csv(BASE_PATH + "movie_tags.dat", sep="\t", encoding="latin1")
tags = pd.read_csv(BASE_PATH + "tags.dat", sep="\t", encoding="latin1").rename(columns={"id": "tagID", "value": "tag"})
movie_tags = movie_tags.merge(tags, on="tagID", how="left")
movie_tags = movie_tags.rename(columns={"movieID": "item_id", "tag": "attribute_value"})
movie_tags["attribute_name"] = "tag"

# -------------------
# Unione tutti gli attributi
# -------------------
all_attrs = pd.concat([
    actors[["item_id", "attribute_name", "attribute_value"]],
    genres[["item_id", "attribute_name", "attribute_value"]],
    directors[["item_id", "attribute_name", "attribute_value"]],
    countries[["item_id", "attribute_name", "attribute_value"]],
    locations[["item_id", "attribute_name", "attribute_value"]],
    movie_tags[["item_id", "attribute_name", "attribute_value"]],
    years[["item_id", "attribute_name", "attribute_value"]],
], ignore_index=True)

all_attrs = all_attrs.dropna(subset=["attribute_value"])
all_attrs = all_attrs[all_attrs["attribute_value"].astype(str).str.strip() != ""]

# -------------------
# Trasformazione in ID numerici
# -------------------
# Mappa attributi (attribute_name + value) a numeri
all_attrs["attr_full"] = all_attrs["attribute_name"] + "__" + all_attrs["attribute_value"]
attr2id = {v: i+1 for i, v in enumerate(all_attrs["attr_full"].unique())}
all_attrs["attribute_value_id"] = all_attrs["attr_full"].map(attr2id)

# Output compatibile Elliot: item_id, attribute_value_id
out_df = all_attrs[["item_id", "attribute_value_id"]]
out_path = BASE_PATH + "../processed/item_attributes.tsv"
out_df.to_csv(out_path, sep="\t", index=False, header=False)

print(f"Creato file con {len(out_df)} attributi totali per {out_df['item_id'].nunique()} film")
