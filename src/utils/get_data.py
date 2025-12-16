# src/utils/get_data.py
import pandas as pd
import os

# URLs des datasets
URLS = {
    "frequentation_mensuelle": "https://www.data.gouv.fr/api/1/datasets/r/4537ed3a-3b96-4416-9d76-148d8d265600",
    "frequentation_region": "https://www.data.gouv.fr/api/1/datasets/r/24ab2a50-814b-4c5e-a6ed-d2497a5b8607",
    "frequentation_hoteliere": "https://www.data.gouv.fr/api/1/datasets/r/459c159d-e575-454f-abec-9718160bbce4"
}

# Répertoire existant où stocker les fichiers
RAW_DIR = "data/raw/"

def load_raw_data():
    dfs = {}
    for name, url in URLS.items():
        print(f"Téléchargement de {name}...")
        df = pd.read_csv(url, sep=";")
        dfs[name] = df
        # Sauvegarde directe dans data/raw/
        df.to_csv(os.path.join(RAW_DIR, f"{name}.csv"), index=False)
        print(f"{name} sauvegardé dans {RAW_DIR}{name}.csv")
    return dfs

if __name__ == "__main__":
    load_raw_data()
