import pandas as pd
import numpy as np
import openai
import requests

from tools import clean_csv
from tqdm.auto import tqdm



# Read data from 
df_fauna = clean_csv('data/EPBC Act List of Threatened Fauna.csv')
df_flora = clean_csv('data/EPBC Act List of Threatened Flora.csv')
df_flora['Group'] = df_flora['Group'].replace('Flora', 'Plants')        # Rename 'Flora' to 'Plants'
df = pd.concat([df_fauna, df_flora], axis=0).reset_index(drop=True)
    

# Get the species names for LUTO 
df_luto = pd.read_excel("N:/Data-Master/Biodiversity/Environmental-suitability/Species-list/species_list.xlsx")
names_luto = df_luto['SPECIES_LUTO'].tolist()






species_names = df_luto['SPECIES_LUTO'].tolist()
base_url = 'https://api.gbif.org/v1/parser/name'

results = []
for name in tqdm(species_names, total=len(species_names)):
    response = requests.get(base_url, params={'name': name})
    if response.status_code == 200:
        results += response.json()


out = pd.DataFrame(results)
out.to_csv('data/species_luto_gbif.csv', index=False)

