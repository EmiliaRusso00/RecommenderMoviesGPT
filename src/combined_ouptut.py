import os

# Cartella contenente i file
folder_path = 'outputChat'

# Ordine dei file da unire
file_order = [
    '8930',
    '1510',
    '70974',
    '36294',
    '52305',
    '32538',
    '62151',
    '21171',
    '6758',
    '63347',
    '71420',
    '39861',
    '50510',
    '68722',
    '13086',
    '67189',
    '40284',
    '34958',
    '24954',
    '2692',
    '35373'
]

# Nome del file finale
output_file = 'combined_output.tsv'

with open(output_file, 'w', encoding='utf-8') as outfile:
    # opzionale: scrivere intestazione TSV
    outfile.write("user_id\ttitle\n")
    
    for user_id in file_order:
        file_path = os.path.join(folder_path, f'{user_id}.txt')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as infile:
                # Legge tutte le righe eliminando righe vuote
                lines = [line.strip() for line in infile if line.strip()]
                for line in lines:
                    outfile.write(f"{user_id}\t{line}\n")
        else:
            print(f"Attenzione: il file {file_path} non esiste, nessun titolo aggiunto.")

print(f"Tutti i file sono stati uniti in {output_file}")
