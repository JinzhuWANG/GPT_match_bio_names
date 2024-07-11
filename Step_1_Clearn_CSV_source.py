import pandas as pd
import numpy as np
import openai

from tools import clean_csv




# Read data
df_fauna = clean_csv('data/EPBC Act List of Threatened Fauna.csv')
df_flora = clean_csv('data/EPBC Act List of Threatened Flora.csv')
df_flora['Group'] = df_flora['Group'].replace('Flora', 'Plants')        # Rename 'Flora' to 'Plants'
df = pd.concat([df_fauna, df_flora], axis=0).reset_index(drop=True)
    

# Get the species names for LUTO 
df_luto = pd.read_excel("N:/Data-Master/Biodiversity/Environmental-suitability/Species-list/species_list.xlsx")
names_luto = df_luto['SPECIES_LUTO'].tolist()



'''
Groups of df    ['Birds', 'Mammals', 'Reptiles', 'Plants', 'Frogs', 'Other Animals', 'Fishes']
Groups of luto  ['Birds', 'Mammals', 'Reptiles', 'Plants', 'Amphibians']
'''

group_same = ['Birds', 'Mammals', 'Reptiles', 'Plants']
group_diff = ['Frogs', 'Other Animals', 'Fishes']

matchs = []
for group in df['Group'].unique():
    
    match_from = df.query('`Group` == @group')['Scientific Name'].tolist()
    
    match_to_df = df_luto.query('TAXON == @group') if group in group_same else df_luto.query('TAXON == "Amphibians"')
    match_to = dict(zip(match_to_df['SPECIES_LUTO'], match_to_df['TAXON']))






# Initialize the OpenAI API key
from openai import OpenAI
client = OpenAI()
n=3
match_from_str = ', '.join(match_from)
match_to_str = ', '.join(match_to.keys())[:15000]

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", 
     "content": '''You are a professor in biology, 
                   skilled in the scientific names and classifications for various species.'''},
    {"role": "user", 
     "content": f'''Find the all matches from the list: '{match_from_str}' 
                    from the following list: {match_to_str}. The match must be from the same group as the original species.
                    Provide the matches and their confidence levels.
                    
                    If you can not find a match, please say 'No match'.'''}
      ]
)

print(completion.choices[0].message.content)


