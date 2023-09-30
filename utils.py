import os
import spacy
import re
import json

def return_each_files_path(subfolder_path):
    for root, _, files in os.walk(subfolder_path):
        for file in files:
            yield os.path.join(root, file)

# Usage example:
# subfolder_path = '/path/to/your/subfolder'
# for path in return_each_files_path(subfolder_path):
#     print(path)


def filter_entities(doc, label):
    filtered_entities = [ent.text for ent in doc.ents if ent.label_ == label]
    return filtered_entities




def save_as_json(data, file_name, subdirectory):
    """
    Save a dictionary or list as a JSON file in a subdirectory.
    If a file with the same name exists, append the data to it.

    Args:
    - data: The dictionary or list to be saved.
    - file_name: The name of the JSON file (without the .json extension).
    - subdirectory: The name of the subdirectory where the JSON file will be saved.

    Returns:
    - The full path to the saved JSON file if successful, or None if there was an error.
    """
    try:
        # Create the subdirectory if it doesn't exist
        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory)

        # Construct the full file path
        file_path = os.path.join(subdirectory, f"{file_name}.json")

        # Initialize existing_data as an empty list if the file doesn't exist
        existing_data = []

        # If the file already exists, load its contents
        if os.path.exists(file_path):
            with open(file_path, 'r') as existing_file:
                existing_data = json.load(existing_file)

        # If data is a dictionary, append it as is; if it's a list, extend the list
        if isinstance(data, dict):
            existing_data.update(data)
        elif isinstance(data, list):
            existing_data.extend(data)

        # Write the combined data to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        print(f"Data saved or appended to {file_path}")
        return file_path  # Return the saved file path
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# # Example usage^:
# data_to_append = {"city": "Los Angeles", "zipcode": "90001"}
# subdirectory_name = "data_folder"

# # Save or append the data to a JSON file in the subdirectory and get the saved path
# saved_path = save_as_json(data_to_append, "person_data", subdirectory_name)
# if saved_path:
#     print(f"Data saved or appended at: {saved_path}")
# else:
#     print("Failed to save or append data.")

class TextProcessor:
    def __init__(self, file_path = r"data\book\krishna volume1.txt", chunksize = 50000):
        self.chunksize = chunksize
        self.file_path = file_path
        self.nlp = spacy.load("en_core_web_sm")

    def read_file(self):
        with open(self.file_path, "r",errors='ignore') as file:
            file_contents = file.read()
        return file_contents

    def clean_text(self, text):
        cleaned_text = re.sub(r'[^a-zA-Z\s.()\'\";,?]', '', text)
        cleaned_text = re.sub(r'[&]', 'and', cleaned_text)
        return cleaned_text

    def tokenize_text(self, text):
        doc = self.nlp(text)
        return doc

    def process_file(self):
        file_contents = self.read_file()
        cleaned_text = self.clean_text(file_contents)
        splitted_text = cleaned_text[:50000]
        #return self.tokenize_text(splitted_text)

        self.chunksize = 50000

        # # Split the document into chunks of 50,000 characters or less
        # print("splitting book into chunks..")
        # book_chunks = [cleaned_text[i:i + self.chunksize] for i in range(0, len(cleaned_text), self.chunksize)]
        # print("tokenising each chunks..")
        # doc_of_each_chunk=[self.tokenize_text(each_chunk) for each_chunk in book_chunks]
        # return doc_of_each_chunk
    
        for i in range(0, len(cleaned_text), self.chunksize):           
            text_chunk = cleaned_text[i:i + self.chunksize]
            yield text_chunk


