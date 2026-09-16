# This is a sample Python practice based on youtube video: https://www.youtube.com/watch?v=uqRRjcsUGgk

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

"""
Python Extract Transform Load Example
"""
import requests
import pandas as pd
from sqlalchemy import (create_engine)

# function to extract data from api
def extract() -> dict:
    API_URL = "http://universities.hipolabs.com/search?country=United+States"
    data = requests.get(API_URL).json()
    return data

# function to transform
def transform(data:dict) -> pd.DataFrame:
    df = pd.DataFrame(data)
    print(f"Total number of universities from API: {len(data)}")
    df = df[df['name'].str.contains("California")]
    print(f"Total number of universities in California: {len(df)}")
    df['domains'] = [','.join(map(str, l)) for l in df['domains']]
    df['web_pages'] = [','.join(map(str, l)) for l in df['web_pages']]
    df = df.reset_index(drop=True)
    return df[['domains', 'web_pages', 'country', 'name']]

def load(df:pd.DataFrame)-> None:
    """ Loads data into a sqllite database"""
    disk_engine = create_engine('sqlite:///my_lite_store.db')
    df.to_sql('cal_uni', disk_engine, if_exists='replace')

# %%
data = extract()
df = transform(data)
load(df)


