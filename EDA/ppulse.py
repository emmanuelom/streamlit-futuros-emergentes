import pandas as pd
import json
import matplotlib.pyplot as plt


def extract_data(filename, sector, keyword):
    # Set file path of patent pulse data
    file_path = f"data_ppulse/{sector}/{filename}"

    with open(file_path) as f:
        data = json.load(f)

    # Extract the relevant data
    extracted_data = []
    for item in data['response']['docs']:
        if 'ww' in item and 'arefd' in item:
            for field in item['ww']:
                if isinstance(item['arefd'], list) and item['arefd']:
                    year = item['arefd'][0][:4]  # Extract the year from 'arefd'
                    extracted_data.append({'Categories': field, 'year': year})

    # Convert the list to a DataFrame
    df = pd.DataFrame(extracted_data)

    # Ensure the 'year' column is of type string (in case of any issues with data type)
    df['year'] = df['year'].astype(str)

    # Get the unique years in the data
    unique_years = sorted(df['year'].unique())

    # Create a pivot table to count the occurrences of 'ww' per year
    pivot_table = pd.pivot_table(df, values='year', index='Categories', columns='year', aggfunc='size', fill_value=0)

    # Add a column for the total count of 'ww' values
    pivot_table['Total'] = pivot_table.sum(axis=1)

    # Create a column that contains the list of counts for each unique year
    pivot_table['All Years'] = pivot_table[unique_years].apply(lambda x: [int(i) for i in x], axis=1)

    # Reorder the columns to have 'Total' and 'All Years' at the beginning
    columns = ['Total', 'All Years'] #+ unique_years
    pivot_table = pivot_table[columns]
    #print(pivot_table.head())

    # Sort the pivot table by the 'Total' column in descending order
    sorted_pivot_table = pivot_table.sort_values(by='Total', ascending=False)

    # Save the sorted pivot table to a CSV file
    sorted_pivot_table.to_csv(f'data/{sector}/ppulse_{keyword}.csv')


# read mapping file
sectors = {'AGROINDUSTRY': 'agroindustry_map.csv'}

for sector, sec_filename in sectors.items():
    print(f"Extracting data from {sector} sector from file {sec_filename}")
    df = pd.read_csv(sec_filename)
    print(df.head())
    keywords = list(df['Node'])
    pp_filenames = list(df['Patent Pulse'])

    for filename, keyword in zip(pp_filenames, keywords):
        extract_data(filename, sector, keyword)
        print(f"Extracted data from {filename}")