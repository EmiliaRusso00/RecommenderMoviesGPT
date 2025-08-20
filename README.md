# 🎬 RecommenderMoviesGPT

Sistema di raccomandazione film basato su modelli di Collaborative Filtering (CF) e GPT, con pipeline di preprocessing, mapping e valutazione.

---

## Requisiti

- **Python 3.8+**  
  Si consiglia di usare un ambiente virtuale (es. `venv` o `conda`).

- **Installazione dipendenze**  
  Dalla cartella `elliot`, installa i requirements:
  ```bash
  pip install -r requirements.txt
  ```

---

## Struttura delle cartelle principali

- **data/**
  - `hetrec2011-movielens-2k-v2/` : Dataset MovieLens originale.
  - `processed/` : Dataset preprocessato:
    - `item_attributes.tsv` : Attributi degli item, utile per alcuni modelli Elliot (generato da `src/creation_info_movie.py`).
    - `ratings_10core.tsv` : Dataset pulito (script `src/preprocessing.py`).
    - `train.tsv` / `test.tsv` : Divisione train/test.

- **elliot/**  
  Framework per la raccomandazione.  
  Contiene i modelli, la logica di training e valutazione.

- **src/**  
  Script di supporto:
  - `creation_info_movie.py` : Genera attributi item.
  - `preprocessing.py` : Pulisce e prepara il dataset.
  - `prompt-RolePlaying.py` : Crea i prompt da inviare a GPT.
  - `combined_ouptut.py` : Combina gli output delle risposte GPT.
  - `mapping.py` : Mappa i titoli ai `item_id` usando RapidFuzz (soglia Gestalt 85%).
  - `metrics.py` : Calcola metriche JBO e RBO tra modelli e GPT.

---

## Esecuzione esperimenti

1. **Preprocessing**  
   Prepara i file in `data/processed` usando gli script in `src/`.

2. **Avvio Elliot**  
   Lancia il framework con:
   ```bash
   python -m elliot.run --config config/config.yml --runner eval
   ```
   - Il file `config/config.yml` contiene la configurazione dei modelli CF da usare.

3. **Pipeline GPT**  
   - Crea i prompt con `prompt-RolePlaying.py`.
   - Invia i prompt a GPT e salva le risposte in `src/prompt-RP/`.
   - Salva gli output della chat in `src/outputChat/`.
   - Combina gli output con `combined_ouptut.py`.
   - Mappa i titoli ai `item_id` con `mapping.py` (matching fuzzy, soglia 85%).
   - Calcola le metriche di confronto tra modelli e GPT con `metrics.py`.

---

## Note

- Alcuni modelli Elliot richiedono `item_attributes.tsv` come input.
- Per dettagli sui modelli e parametri, consulta `config/config.yml`.
- 
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
