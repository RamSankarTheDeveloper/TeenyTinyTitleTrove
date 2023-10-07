import config
import os
import json

def inner_dict():
    file_path = config.paths["complete_dictionary"]
    with open(file_path, 'r') as json_file:
        dict = json.load(json_file)
        for key,inner_dict in dict.items():
            return inner_dict

word_list = [key for key,pair in inner_dict().items()]
sorted_list = sorted(word_list, key=lambda x: len(x))

output_directory = config.paths["sorted_by_length"] #r"data\results\distance\each names"
os.makedirs(output_directory, exist_ok=True)

json_filename = os.path.join(output_directory, "sorted by length.json")

# Save the sorted keys as a JSON file
with open(json_filename, "w") as json_file:
    json.dump(sorted_list, json_file)