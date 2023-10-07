import json
import os 
import config

# Step 1: Read the dictionary from the file path
file_path = config.paths["complete_dictionary"]
with open(file_path, 'r') as json_file:
    original_dict = json.load(json_file)

sorted_dict = {}

# Iterate through the original dictionary
for key, inner_dict in original_dict.items():
    # Sort the inner dictionary by values in ascending order
    sorted_items = sorted(inner_dict.items(), key=lambda x: x[1])

    # Extract the keys from sorted items
    sorted_keys = [item[0] for item in sorted_items]

    # Add the sorted keys to the new dictionary
    sorted_dict[key] = sorted_keys




# Save the reformatted dictionary to the specified file path
# with open(os.path.join('data_christian','results','distance','cleaned names.json'), 'w') as json_file:
#     json.dump(sorted_dict, json_file)

# Save the reformatted dictionary to the specified file path
output_directory = config.paths["individual names"] #r"data\results\distance\each names"
os.makedirs(output_directory, exist_ok=True)

# Iterate through the original dictionary
for key, inner_dict in original_dict.items():
    # Sort the inner dictionary by values in ascending order
    sorted_items = sorted(inner_dict.items(), key=lambda x: x[1])

    # Extract the keys from sorted items
    sorted_keys = [item[0] for item in sorted_items]

    # Create a JSON filename
    json_filename = os.path.join(output_directory, f"{key}.json")

    # Save the sorted keys as a JSON file
    with open(json_filename, "w") as json_file:
        json.dump(sorted_keys, json_file)