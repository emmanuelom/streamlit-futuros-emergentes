import pandas as pd

filenames = ["data_scopus/scopus_ai_farming_cs.csv", "data_scopus/scopus_ai_farming_eng.csv"]
areas = ["Computer Science", "Engineering"]


frames = []
for filename, area in zip(filenames, areas):
    df = pd.read_csv(filename)
    df["Subject area"] = area
    frames.append(df)

result = pd.concat(frames)
print(result.head(10))
print(result.tail(10))


# Get the unique years in the data
unique_years = sorted(result['Year'].unique())

# Create a pivot table to count the occurrences of 'Subject area' per year
pivot_table = pd.pivot_table(result, index='Year', columns='Subject area', aggfunc='size', fill_value=0).T

# Add a column for the total count of 'Subject area' values
pivot_table['Total'] = pivot_table.sum(axis=1)

print(pivot_table)

