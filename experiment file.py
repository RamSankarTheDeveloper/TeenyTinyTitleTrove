import spacy
import re
import json
import os
import utils


# class to enter a subfolder path that yields a doc format that envelopes text_preprocessor,below two classes (non-reusable)

# class to save as file that enveopes above class (reusable)

# function to filter by ner if given a chunk(re-usable)

#make a class that if input a folder name, it will give the 

class WordCollector:
    def __init__(self,input_folder= ["data", "book"], output_folder= ['data','collected words'],entity_lists=['PERSON']):
        book_directory_parts = input_folder
        self.book_directory = os.path.join(*book_directory_parts)
        self.nlp = spacy.load("en_core_web_sm")
        self.directory_to_save_collected_words = os.path.join(*output_folder)

    def book_chunking(self):
        for each_book_path in utils.return_each_files_path(self.book_directory):
            text_processor = utils.TextProcessor(each_book_path)
            for text_chunk in text_processor.process_file():
                yield text_chunk

    def extract_and_save_NER_from_text(self,text_chunk):#ENTITY CHANGE        
        doc_chunk = self.nlp(text_chunk)
        person_names =list(set([ent.text for ent in doc_chunk.ents if ent.label_ == 'PERSON']))
        return ( 'person_names',person_names)
        
    def remove_duplicates_from_json(self,json_file_path):
        try:
            # Open the JSON file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            # Check if data is a list
            if isinstance(data, list):

                def preprocess_json_list_data(data):
                    data = [word.lower() for word in data]
                    # Remove duplicates while preserving order (Python 3.7+)
                    data = list(dict.fromkeys(data))
                    return data
                data= preprocess_json_list_data(data)
                

                # Re-save the JSON file with duplicates removed
                with open(json_file_path, 'w') as updated_json_file:
                    json.dump(data, updated_json_file, indent=4)
                
                print(f"Duplicates removed from {json_file_path}")

        except Exception as e:
            print(f"An error occurred while processing {json_file_path}: {str(e)}")

    def process(self):  #main file that is not resuable. others int this classes is slightly reusable
        # for each_text_chunk in self.book_chunking():
        #     file_name,file = self.extract_and_save_NER_from_text(text_chunk= each_text_chunk)
        #     utils.save_as_json(data= file, file_name= file_name, subdirectory= self.directory_to_save_collected_words)
        self.remove_duplicates_from_json(os.path.join(self.directory_to_save_collected_words,'person_names.json'))



if __name__ == "__main__":
    WordCollector().process()




