import os
import pandas as pd
from collections import defaultdict
from rbo import RankingSimilarity

# Cartella con i risultati dei modelli
results_folder = '../results/movielens_baseline/recs'

# File delle raccomandazioni ChatGPT senza header
user_items_file = 'outputChat/user_item_ids.tsv'
user_items_df = pd.read_csv(
    user_items_file, sep='\t', header=None, names=['user_id', 'item_id']
)

# Creiamo lista di item per ciascun utente, mantenendo ordine e sostituendo duplicati con None
true_items_list = []
current_user = None
seen_items = set()
current_items = []

for _, row in user_items_df.iterrows():
    if row['user_id'] != current_user:
        if current_user is not None:
            true_items_list.append(current_items)
        current_user = row['user_id']
        seen_items = set()
        current_items = []

    item = row['item_id']
    if pd.notna(item):
        if item in seen_items:
            current_items.append(None)  # duplicato -> campo vuoto
        else:
            current_items.append(item)
            seen_items.add(item)
    else:
        current_items.append(None)  # campo vuoto già presente
# aggiungiamo l'ultimo utente
true_items_list.append(current_items)

# Funzione Jaccard
def jaccard(set1, set2):
    if not set1 and not set2:
        return 1.0
    return len(set1 & set2) / len(set1 | set2)

# Ciclo su tutti i file modello
for file in os.listdir(results_folder):
    if file.endswith('.tsv') or file.endswith('.csv'):
        model_file = os.path.join(results_folder, file)
        df = pd.read_csv(model_file, sep='\t', header=None, names=['user_id', 'item_id', 'score'])

        # Prendiamo solo le prime 1050 righe (21 utenti * 50 righe)
        df = df.head(1050)

        # Creiamo lista di item predetti per ciascun utente, sostituendo duplicati con None
        pred_items_list = []
        current_user = None
        seen_items = set()
        current_items = []

        for _, row in df.iterrows():
            if row['user_id'] != current_user:
                if current_user is not None:
                    pred_items_list.append(current_items)
                current_user = row['user_id']
                seen_items = set()
                current_items = []

            item = row['item_id']
            if pd.notna(item):
                if item in seen_items:
                    current_items.append(None)
                else:
                    current_items.append(item)
                    seen_items.add(item)
            else:
                current_items.append(None)
        pred_items_list.append(current_items)

        # Calcolo metriche
        jaccard_scores = []
        rbo_scores = []

        for true_items, pred_items in zip(true_items_list, pred_items_list):
            # Jaccard: ignoriamo i None
            true_set = set([x for x in true_items if x is not None])
            pred_set = set([x for x in pred_items if x is not None])
            j_score = jaccard(true_set, pred_set)
            jaccard_scores.append(j_score)

            # RBO: eliminiamo None e duplicati dai true_items, pred_items mantiene ordine
            r = RankingSimilarity(
                [x for x in pred_items if x is not None],
                list(dict.fromkeys([x for x in true_items if x is not None]))
            )
            r_score = r.rbo(p=0.9)
            rbo_scores.append(r_score)

        print(f'Model: {file}')
        print(f'Avg Jaccard: {sum(jaccard_scores)/len(jaccard_scores):.4f}')
        print(f'Avg RBO: {sum(rbo_scores)/len(rbo_scores):.4f}\n')
