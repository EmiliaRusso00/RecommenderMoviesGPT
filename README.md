# 🎬 RecommenderMoviesGPT

Sistema di raccomandazione di film basato su **Collaborative Filtering (CF)** e **GPT-4.0**, con pipeline completa di **preprocessing**, **mapping** e **valutazione**.

---

##  Requisiti

- **Python 3.8+**  
  Consigliato l’uso di un ambiente virtuale (`venv` o `conda`).

- **Installazione dipendenze**  
  Dalla cartella `elliot`, installare i requirements:
  ```bash
  pip install -r requirements.txt

📂 Struttura del progetto
Cartella	Contenuto
data/	Dati originali e preprocessati
├── hetrec2011-movielens-2k-v2/	Dataset MovieLens originale
└── processed/	Dataset preprocessato:
• item_attributes.tsv → Attributi item (da creation_info_movie.py)
• ratings_10core.tsv → Dataset pulito (preprocessing.py)
• train.tsv / test.tsv → Split train/test
elliot/	Framework per modelli di raccomandazione, training e valutazione
src/	Script di supporto:
• creation_info_movie.py → Genera attributi item
• preprocessing.py → Pulizia/preparazione dataset
• prompt-RolePlaying.py → Generazione prompt GPT
• combined_output.py → Combina risposte GPT
• mapping.py → Mapping titoli → item_id (RapidFuzz, soglia 85%)
• metrics.py → Calcolo metriche Jaccard e RBO

Esecuzione esperimenti
1️⃣ Preprocessing
Genera i file preprocessati in data/processed:
python src/preprocessing.py

2️⃣ Avvio Elliot
Esegui i modelli CF:
python -m elliot.run --config config/config.yml --runner eval
📌 Configurazioni dei modelli in config/config.yml.

3️⃣ Pipeline GPT
Genera prompt → prompt-RolePlaying.py
Invia i prompt a GPT → salva risposte in src/prompt-RP/
Esporta output → src/outputChat/
Combina risposte → combined_output.py
Mapping titoli → mapping.py (fuzzy, soglia 85%)
Calcolo metriche → metrics.py

📝 Note
Alcuni modelli Elliot richiedono item_attributes.tsv.
Parametri e modelli personalizzabili in config/config.yml.
---
## 📖 Riferimenti e ispirazioni

Questo progetto è un **riadattamento semplificato** del lavoro presentato in:

**Paper**  
*Content-Based or Collaborative? Insights from Inter-List Similarity Analysis of ChatGPT Recommendations*  
Dario Di Palma, Giovanni Maria Bianco, Fedelucio Narducci, Vito Walter Anelli, Tommaso Di Noia  
[DOI: 10.1145/3708319.3733680](https://doi.org/10.1145/3708319.3733680)

**Repository originale**  
👉 [sisinflab/Content-or-Collaborative-](https://github.com/sisinflab/Content-or-Collaborative-.git)

---

### 🔹 Differenze principali rispetto al lavoro originale
-  **Dataset**: questo progetto utilizza un unico dataset → [MovieLens HetRec 2011](https://grouplens.org/datasets/hetrec-2011/).  
-  **Prompting**: viene adottata una singola modalità → **Role Playing**.  
-  **Pipeline**: semplificata rispetto all’implementazione completa del paper.  

L’obiettivo è fornire una versione **leggera e riproducibile** degli esperimenti, mantenendo la logica centrale del confronto tra **Collaborative Filtering (CF)** e **raccomandazioni GPT** tramite metriche di similarità (Jaccard e RBO).
