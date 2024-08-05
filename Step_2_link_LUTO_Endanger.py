import pandas as pd


# Read data
species_luto_raw = pd.read_csv('data/species_luto_raw.csv')[['SPECIES_LUTO', 'TAXON']]
species_endanger_raw = pd.read_csv('data/species_endanger_raw.csv')[['Scientific Name', 'Endangered Status']]

species_luto_gbif = pd.read_csv('data/species_luto_gbif.csv')[['scientificName', 'canonicalName']]
species_endanger_gbif = pd.read_csv('data/species_endanger_gbif.csv')[['scientificName', 'canonicalName']]


# Merge `canonicalName` to the raw data
species_luto_complete = species_luto_raw.merge(species_luto_gbif, left_on='SPECIES_LUTO', right_on='scientificName', how='left')
species_endanger_complete = species_endanger_raw.merge(species_endanger_gbif, left_on='Scientific Name', right_on='scientificName', how='left')



# Link luto with endanger data by `canonicalName`
'''
Num. of LUTO species: 10691
Num. of EPBC Endanger species: 2106
Num. of LUTO species matches EPBC Endanger species: 326
'''
species_luto_endanger = species_luto_complete.merge(
    species_endanger_complete, 
    left_on='canonicalName',
    right_on='canonicalName', 
    how='left')



species_luto_endanger.to_csv('data/species_luto_endanger.csv', index=False)




















