import os
import re


def remove_timestamp(folder_path):
    # Regular expression to match the timestamp
    pattern = r'\d{14}'

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the filename contains a timestamp
        if re.search(pattern, filename):
            # Substitute the timestamp with an empty string
            new_filename = re.sub(pattern, '', filename)
            
            # Get full file paths
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, new_filename)
            
            # Rename the file
            os.rename(old_file, new_file)
            
            print(f'Renamed: {filename} to {new_filename}')

folder_path = "data_ppulse/AGROINDUSTRY"
remove_timestamp(folder_path)

#for filename in os.listdir(folder_path):
#    print(filename)



'''
import json

# File paths
input_file = 'input.json'
output_file = 'output.json'

# Read the JSON file as a string
with open(input_file, 'r') as file:
    data = file.read()

def remove_key1(data, key1, key2):
    # Find the key in the data
    start_index1 = data.find(f'"{key1}":')
    start_index2 = data.find(f'"{key2}":')
    if start_index1 == -1:
        return data  # Key not found

    removed_data = data[start_index1:start_index2]
    print(removed_data)

    # Replace the old value with the new value
    new_data = data[:start_index1-1] + data[start_index2:]

    return new_data

# Update the JSON string
updated_data = remove_key1(data, "name", "created")

# Write the modified string back to the JSON file
with open(output_file, 'w') as file:
    file.write(updated_data)

print("Updated JSON file saved as", output_file)
'''