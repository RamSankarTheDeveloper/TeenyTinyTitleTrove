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
        self.book_directory_for_stories = os.path.join("data", "book",'story books')
        self.book_directory_for_namebooks = os.path.join("data", "book",'name books')
        self.nlp = spacy.load("en_core_web_sm")
        self.directory_to_save_collected_words = os.path.join(*output_folder)

    def books_chunking(self,directory):
        for each_book_path in utils.return_each_files_path(directory):
            text_processor = utils.TextProcessor(each_book_path)
            for text_chunk in text_processor.process_file():
                yield each_book_path, text_chunk

    def extract_NER_from_text(self,text_chunk):#ENTITY CHANGE        
        doc_chunk = self.nlp(text_chunk)
        person_names =list(set([ent.text for ent in doc_chunk.ents if ent.label_ 
                                #== 'PERSON']
                                not in ("DATE", "TIME", "MONEY", "PERCENT")
                                ]))
        return ( 'person_names',person_names)
    
    def extract_tokens_from_text(self,text_chunk):      
        doc_chunk = self.nlp(text_chunk)
        person_names =list(set([token.text for token in doc_chunk]))
        return ( 'person_names',person_names)
        
    def preprocess_names_in_json(self,json_file_path):
        try:
            # Open the JSON file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            # Check if data is a list
            if isinstance(data, list):

                def clean_collected_names(data):
                    
                    data = [word.lower() for word in data]
                    data = [word.replace(r'\n.*','') for word in data]
                    data = [word.replace("'s",' ') for word in data]
                    data = [word.lower() for word in data]
                    def clean_word(word):
                        return re.sub(r'[^a-zA-Z\s]', ' ', word)
                    data = [clean_word(word) for word in data]

                    #data = [word.replace(r'.',' ') for word in data]
                    data = [word.strip() for word in data]

                    data = [word for word in data if word != ""]

                    # Remove duplicates while preserving order (Python 3.7+)
                    data = list(dict.fromkeys(data))
                    return data
                data= clean_collected_names(data)
                

                # Re-save the JSON file with duplicates removed
                with open(json_file_path, 'w') as updated_json_file:
                    json.dump(data, updated_json_file, indent=4)
                
                print(f"Duplicates removed from {json_file_path}")

        except Exception as e:
            print(f"An error occurred while processing {json_file_path}: {str(e)}")

    
    def process(self):  #main file that is not resuable. others int this classes is slightly reusable
        for each_folder in [self.book_directory_for_stories,self.book_directory_for_namebooks]:
            if each_folder == self.book_directory_for_stories:
                for book_path, each_text_chunk in self.books_chunking(self.book_directory_for_stories):
                    print(f'accessing book chunk..')
                    file_name,file = self.extract_NER_from_text(text_chunk= each_text_chunk)
                    utils.save_as_json(data= file, file_name= file_name, subdirectory= self.directory_to_save_collected_words)
                    print("opened_file= ", book_path)
            if each_folder == self.book_directory_for_namebooks:
                for book_path, each_text_chunk in self.books_chunking(self.book_directory_for_namebooks):
                    file_name,file = self.extract_tokens_from_text(text_chunk= each_text_chunk)
                    utils.save_as_json(data= file, file_name= file_name, subdirectory= self.directory_to_save_collected_words)
                    print("opened_file= ", book_path)
            
        self.preprocess_names_in_json(os.path.join(self.directory_to_save_collected_words,'person_names.json'))



if __name__ == "__main__":
    WordCollector().process()




