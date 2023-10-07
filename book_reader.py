import spacy
import re
import json
import os
import utils
import json_edit
import config


# class to enter a subfolder path that yields a doc format that envelopes text_preprocessor,below two classes (non-reusable)

# class to save as file that enveopes above class (reusable)

# function to filter by ner if given a chunk(re-usable)

#make a class that if input a folder name, it will give the 

class WordCollector:
    def __init__(self,input_folder= ['data_christian', "book"], directory_to_save_collected_words= config.paths["collected_words_path"],entity_lists=['PERSON']):
        self.book_directory_for_stories = config.paths["book_directory_for_stories"]
        self.book_directory_for_namebooks = config.paths["book_directory_for_namebooks"]
        self.nlp = spacy.load("en_core_web_lg",disable=["tagger", "parser", "textcat"])
        self.directory_to_save_collected_words = directory_to_save_collected_words
        utils.create_folder_if_not_exists(self.book_directory_for_stories)
        utils.create_folder_if_not_exists(self.book_directory_for_namebooks)
        utils.create_folder_if_not_exists(self.directory_to_save_collected_words)
        self.textprocessor=utils.TextProcessor()

    def books_chunking(self,directory):
        for each_book_path in utils.return_each_files_path(directory):
            text_process = self.textprocessor.process_file(each_book_path)
            for text_chunk in text_process:
                yield each_book_path, text_chunk

    def extract_NER_from_text(self,text_chunk):#ENTITY CHANGE        
        doc_chunk = self.nlp(text_chunk)
        names =list(set([ent.text for ent in doc_chunk.ents if ent.label_ 
                                #== 'PERSON']
                                #not in ("DATE", "TIME", "MONEY", "PERCENT")
                                in config.reqd_entity_labels
                                ]))
        return ( 'person_names',names)
    
    def extract_tokens_from_text(self,text_chunk):      
        doc_chunk = self.nlp(text_chunk)
        person_names =list(set([token.text for token in doc_chunk]))
        return ( 'person_names',person_names)

    
    def process(self):  #main file that is not resuable. others int this classes is slightly reusable
        book_path_check=''
        def is_changed_book(book_path_check,book_path):
            if book_path_check =='':
                book_path_check=book_path
            else:
                if book_path_check== book_path:
                    pass
                elif book_path_check!=book_path:
                    return True
            return False
                    


        for each_folder in [self.book_directory_for_stories,self.book_directory_for_namebooks]:
            if each_folder == self.book_directory_for_stories:
                for book_path, each_text_chunk in self.books_chunking(self.book_directory_for_stories):
                    print(f'accessing book chunk..')
                    file_name,file = self.extract_NER_from_text(text_chunk= each_text_chunk)
                    utils.save_as_json(data= file, file_name= file_name, subdirectory= self.directory_to_save_collected_words)
                    print("opened_file= ", book_path)
                    # if is_changed_book(book_path_check,book_path):
                    #     utils.move_file(self.book_directory_for_stories+os.sep+)


            if each_folder == self.book_directory_for_namebooks:
                for book_path, each_text_chunk in self.books_chunking(self.book_directory_for_namebooks):
                    file_name,file = self.extract_tokens_from_text(text_chunk= each_text_chunk)
                    utils.save_as_json(data= file, file_name= file_name, subdirectory= self.directory_to_save_collected_words)
                    print("opened_file= ", book_path)
        
        json_edit.CollectedNameProcessor(json_path= config.paths['person_names'],
                                      save_path= config.paths['person_names']).execute()




if __name__ == "__main__":
    WordCollector().process()
    #WordCollector()



"""    
    nlp = spacy.load("en_core_web_lg")
    print(nlp.get_pipe("ner").labels)  #to get the label names

    CARDINAL: Cardinal numbers (e.g., "one," "two," "three").

    DATE: Dates expressed in various formats (e.g., "January 1, 2022").

    EVENT: Events, such as festivals, ceremonies, or gatherings.

    FAC (Facility): Names of facilities or buildings, such as airports or stadiums.

    GPE (Geo-Political Entity): Geopolitical locations, such as countries, cities, states, and provinces.

    LANGUAGE: Names of languages.

    LAW: References to laws or legal documents.

    LOC (Location): General locations or areas.

    MONEY: Currency amounts (e.g., "$100" or "€50").

    NORP (Nationalities or Religious/Political Groups): Names of nationalities, religious groups, or political affiliations.

    ORDINAL: Ordinal numbers (e.g., "first," "second," "third").

    ORG (Organization): Names of companies, organizations, institutions, etc.

    PERCENT: Percentage values (e.g., "20%").

    PERSON: Names of people, including first and last names.

    PRODUCT: Names of products or items.

    QUANTITY: Measurements or quantities (e.g., "5 kilometers" or "10 pounds").

    TIME: Times expressed in various formats (e.g., "3:30 PM").

    WORK_OF_ART: Titles of artistic or literary works, such as books, songs, or paintings."""
