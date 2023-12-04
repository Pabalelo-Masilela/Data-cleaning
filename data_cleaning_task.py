''' Load store_income_data_task.csv.
    Take a look at all the unique values in the "country" column. Then, convert
    the column entries to lowercase and remove any trailing white spaces.
    Clean up the “country” column so that there are three distinct countries.
    Create a new column called `days_ago` in the DataFrame that is a copy of
    the “date_measured” column but instead shows a number that represents the number of days ago that it was measured. '''

import pandas as pd
from datetime import datetime
import fuzzywuzzy as fz
from fuzzywuzzy import process

# Load the data to be read from the store data CSV
df = pd.read_csv('store_income_data_task.csv', sep=',', quotechar='"')

# Lowercase and remove empty trailing spaces for country entries to create a sort of uniformity
df['country'] = df['country'].str.lower()
df['country'] = df['country'].str.strip()
df['country'] = df['country'].str.strip('/')
df['country'] = df['country'].str.strip('.')

# Function to parse country column to replace high matches with uniform country code
def string_match_replace(df, column, string_to_match, min_ratio=90):
    # Get a list of unique strings
    strings = df[column].unique()

    # Get the top 10 closest matches to our input string
    matches = fz.process.extract(string_to_match, strings, scorer=fz.fuzz.token_sort_ratio)

    # Only get matches with a ratio > 90
    accepted_matches = [match[0] for match in matches if match[1] >= min_ratio]

    # Get the rows of all the close matches in our DataFrame
    rows_with_matches = df[column].isin(accepted_matches)

    # Replace all rows with close matches with the input matches 
    df.loc[rows_with_matches, column] = string_to_match
    
    # Let us know when the function is done
    print(matches)
    print("Matches converted!")

# Call the function to replace country names
string_match_replace(df=df, column='country', string_to_match="united kingdom")
string_match_replace(df=df, column='country', string_to_match="united states of america")
string_match_replace(df=df, column='country', string_to_match="south africa")
string_match_replace(df=df, column='country', string_to_match="britain")

# Additional replacements
df.replace('america', 'united states of america', inplace=True)
df.replace('united states', 'united states of america', inplace=True)
df.replace('united  states of america', 'united states of america', inplace=True)
df.replace('britain', 'united kingdom', inplace=True)
df.replace('u.k', 'united kingdom', inplace=True)
df.replace('uk', 'united kingdom', inplace=True)
df.replace('england', 'united kingdom', inplace=True)
df.replace('s.a', 'south africa', inplace=True)
df.replace('sa', 'south africa', inplace=True)
df.replace('s. africasouth africa', 'south africa', inplace=True)

# Drop rows with missing or empty country names
df = df[df['country'].notna() & (df['country'] != '')]


# Convert the 'date_measured' column to datetime format
df['date_measured'] = pd.to_datetime(df['date_measured'], format='%d-%m-%Y')

# Calculate the number of days ago and create the 'days_ago' column
df['days_ago'] = (datetime.now() - df['date_measured']).dt.days

# View unique country entries and the new 'days_ago' column
print(f"Count of unique country entries: {len(df['country'].unique())}\n ***********")
print(df[['country', 'days_ago']])
