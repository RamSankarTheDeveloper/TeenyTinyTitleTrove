import json

with open("word_dist_dict_all.json", "r") as json_file:
    # Load the JSON data into a dictionary
    word_dist_dict = json.load(json_file)

sorted_dict = dict(sorted(word_dist_dict.items(), key=lambda item: item[1]))

# Print the sorted dictionary
print(sorted_dict)