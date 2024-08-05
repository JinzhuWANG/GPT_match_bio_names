import requests
import pandas as pd
from tqdm.auto import tqdm



# Read data
'''
Num. of LUTO species: 10691
Num. of EPBC Endanger species: 2106
Num. of LUTO species matches EPBC Endanger species: 326
'''
species_luto_endanger = pd.read_csv('data/species_luto_endanger.csv')


# IUCN Red List API key
headers = {
        'Authorization': 'm3qnhz8EXh895G4Cks2qf3kzxLwBKxtXq9t3'
    }


# Funtion to get assessment id
def get_assessment_id(full_name):
    # Base URL for the GET request
    url = f'https://api.iucnredlist.org/api/v4/taxa/scientific_name'
    # Create the parameters for the GET request
    genus_name, species_name = full_name.split(' ')
    params = {
        'genus_name': genus_name,
        'species_name': species_name
        }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        assess_id = data['assessments'][0]['assessment_id'] if len(data['assessments']) > 0 else None
        return assess_id
    else:
        print(f'Can not find record for {full_name} in the RedList. (Error code: {response.status_code})')
        return None
    
    
# Function to get the conservation status of a species
def get_assessment_value(assess_id):
    # Base URL for the GET request
    url = f'https://api.iucnredlist.org/api/v4/assessment/{assess_id}'
    # Make the GET request
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data['red_list_category']['code']
    else:
        return None
    
    
    
# Get the conservation status of each species
endanger_status = []
for _, row in tqdm(species_luto_endanger.iterrows(), total=species_luto_endanger.shape[0]):
    full_name = row['canonicalName']
    assess_id = get_assessment_id(full_name)
    if assess_id:
        assess_val = get_assessment_value(assess_id)
        endanger_status.append(assess_val)
    else:
        endanger_status.append(None)
        
        
# Add the conservation status to the DataFrame
species_luto_endanger['Endanger Status IUCN'] = endanger_status
species_luto_endanger.to_csv('data/species_luto_endanger_iucn.csv', index=False)





