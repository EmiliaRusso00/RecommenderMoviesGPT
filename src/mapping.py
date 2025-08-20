import pandas as pd
import re
import unicodedata
from rapidfuzz import process, fuzz

# ====== Percorsi ======
csv_file = "combined_output.tsv"   # contiene user_id, title
movies_file = "../data/hetrec2011-movielens-2k-v2/movies.dat"
output_file = "outputChat/user_item_ids.tsv"

# ====== Parametri ======
SIM_THRESHOLD = 85

# ====== Normalizzazione titoli ======
def normalize_title(title: str) -> str:
    title = str(title).lower()
    title = re.sub(r"\(\d{4}\)", "", title)  # rimuove anni tra parentesi
    title = "".join(
        c for c in unicodedata.normalize("NFD", title)
        if unicodedata.category(c) != "Mn"
    )  # rimuove accenti
    title = re.sub(r"[^a-z0-9\s]", " ", title)  # tieni solo lettere/numeri
    title = re.sub(r"\s+", " ", title).strip()
    return title

# ====== Carica i dati ======
df = pd.read_csv(csv_file, sep="\t", encoding="utf-8")
movies = pd.read_csv(movies_file, sep="\t", encoding="latin-1")

# Normalizza titoli in movies.dat
movies["title_norm"] = movies["title"].apply(normalize_title)
title_to_id = dict(zip(movies["title_norm"], movies["id"]))
all_titles = list(movies["title_norm"])

# ====== Funzione mapping ======
def map_title_to_id(title: str):
    if pd.isna(title) or not str(title).strip():
        return ""
    title_norm = normalize_title(title)

    # match fuzzy: prova diverse metriche
    match = process.extractOne(
        title_norm,
        all_titles,
        scorer=fuzz.token_set_ratio   # più robusto rispetto a token_sort_ratio
    )

    if match and match[1] >= SIM_THRESHOLD:
        return title_to_id[match[0]]
    return ""

# ====== Applica mapping ======
df["item_id"] = df["title"].apply(map_title_to_id)
df_final = df[["user_id", "item_id"]]

# ====== Salva risultato ======
df_final.to_csv(output_file, sep="\t", index=False, encoding="utf-8")
print(f"File finale creato: {output_file}")

# ====== Debug: quanti match mancanti ======
missing_count = (df_final["item_id"] == "").sum()
print(f"Numero di titoli senza item_id: {missing_count}")

# Mostra alcuni esempi di match falliti per debug
unmatched = df[df_final["item_id"] == ""].head(10)
if not unmatched.empty:
    print("\nEsempi di titoli non mappati:")
    print(unmatched[["user_id", "title"]])
