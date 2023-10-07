import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import json
from itertools import chain
import re
import utils
import config

nltk.download("stopwords")
nltk.download("wordnet")

class CollectedNameProcessor:
    def __init__(self, 
                 json_path= config.paths['person_names'],
                 save_path= config.paths['person_names']):
        utils.create_folder_if_not_exists(json_path)
        utils.create_folder_if_not_exists(save_path)
        self.json_path = json_path
        self.save_path = save_path

    def extract_list_from_json(self, json_path):
        with open(json_path, "r") as json_file:
            data = json.load(json_file)
        if isinstance(data, list):
            return data
        else:
            raise ValueError("JSON file does not contain a list.")
        
    def flatten_list(self,list_data):
        list_data = list(chain.from_iterable([word.split() for word in list_data])) #convert each item in list to a list, flattened by chain
        return list_data
        
    def remove_english_from_list(self, list_data):
        def has_synonyms(word):
            # Get WordNet synsets for the word
            synsets = wordnet.synsets(word)
            # If there are multiple synsets, it has synonyms
            return len(synsets) > 1
        if config.religion not in config.settings['synsets_off_religions']:
            list_data = [word for word in list_data if not has_synonyms(word)]
        stop_words = set(stopwords.words('english'))
        list_data = [word for word in list_data if not word in stop_words]

        return list_data
    
    def clean_items(self,list_data):
        def clean_word(word):
            return re.sub(r'[^a-zA-Z\s]', ' ', word)
        list_data = [word.lower() for word in list_data]
        list_data = [word.replace(r'\n.*','') for word in list_data]
        list_data = [word.replace("'s",' ') for word in list_data]
        list_data = [word.lower() for word in list_data]
        list_data = [clean_word(word) for word in list_data]
        #list_data = [word.replace(r'.',' ') for word in list_data]
        list_data = [word.strip() for word in list_data]
        list_data = [word for word in list_data if word != ""]
        # Remove duplicates while preserving order (Python 3.7+)
        list_data = list(dict.fromkeys(list_data))
        return list_data
    
    def save_as_json(self,list_data, save_path=config.paths['person_names']):
        with open(save_path, 'w') as updated_json_file:
            json.dump(list_data, updated_json_file, indent=4)

    def execute(self):
         list_data = self.extract_list_from_json(self.json_path)
         list_data = self.flatten_list(list_data)
         list_data = self.clean_items(list_data)
         list_data = self.remove_english_from_list(list_data)
         list_data = self.clean_items(list_data)
         self.save_as_json(list_data,save_path= self.save_path)
         




if __name__ == "__main__":
    CollectedNameProcessor()
    #utils.create_folder_if_not_exists(config.paths['person_names'])