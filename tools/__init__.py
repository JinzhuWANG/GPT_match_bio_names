import re

import pandas as pd
import numpy as np


def clean_csv(path:str):

    # Read and name the columns
    df = pd.read_csv(path, header=None)
    df.columns = ['Scientific Name', 'Common Name']
    df['Scientific Name'] = df['Scientific Name'].str.replace('\xa0', ' ')

    # Remove unnecessary heading rows
    rm_head = 'Genus, species (subspecies, population)'
    df = df.query('`Scientific Name` != @rm_head').reset_index(drop=True)

    # Get the heading and rows of the same endangered status
    endangered = df.query('`Scientific Name`.str.contains("that are")')
    split_idx = np.array_split(df.index, endangered.index[1:])

    clearn_df = pd.DataFrame()
    for desc, idx in zip(endangered['Scientific Name'], split_idx):
        # Select the rows of the same species and endangered status
        sel_df = df.iloc[idx[1:]].copy()
        
        # Extract the species and endangered status, append to the dataframe
        group = re.compile(r'(.*?) that are').findall(desc)[0]   # Characters before 'that are'
        status = re.compile(r'that are (.*?) ').findall(desc)[0]   # Characters between 'that are' and ' '
        sel_df['Endangered Status'] = status
        sel_df['Group'] = group
        
        # Append to the final dataframe
        clearn_df = pd.concat([clearn_df, sel_df], axis=0)
        
    return clearn_df