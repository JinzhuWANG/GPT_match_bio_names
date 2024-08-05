import pandas as pd
import numpy as np
import requests

from tools import clean_csv
from tqdm.auto import tqdm



# Read data from Environment Protection and Biodiversity Conservation (EPBC)
df_fauna = clean_csv('data/EPBC Act List of Threatened Fauna.csv')
df_flora = clean_csv('data/EPBC Act List of Threatened Flora.csv')
df_flora['Group'] = df_flora['Group'].replace('Flora', 'Plants')        # Rename 'Flora' to 'Plants'
df = pd.concat([df_fauna, df_flora], axis=0).reset_index(drop=True)
df.to_csv('data/species_endanger_raw.csv', index=False)
    

# Get the species names for LUTO 
df_luto = pd.read_excel("N:/Data-Master/Biodiversity/Environmental-suitability/Species-list/species_list.xlsx")
df_luto.to_csv('data/species_luto_raw.csv', index=False)
names_luto = df_luto['SPECIES_LUTO'].tolist()





###### Search for species in LUTO
species_names = df_luto['SPECIES_LUTO'].tolist()
base_url = 'https://api.gbif.org/v1/parser/name'

results = []
for name in tqdm(species_names, total=len(species_names)):
    response = requests.get(base_url, params={'name': name})
    if response.status_code == 200:
        results += response.json()


species_luto_gbif = pd.DataFrame(results)
species_luto_gbif.to_csv('data/species_luto_gbif.csv', index=False)




####### Search for endangered species in the GBIF database
species_names = df['Scientific Name'].tolist()
base_url = 'https://api.gbif.org/v1/parser/name'

results = []
for name in tqdm(species_names, total=len(species_names)):
    response = requests.get(base_url, params={'name': name})
    if response.status_code == 200:
        results += response.json()


species_endanger_gbif = pd.DataFrame(results)
species_endanger_gbif.to_csv('data/species_endanger_gbif.csv', index=False)


