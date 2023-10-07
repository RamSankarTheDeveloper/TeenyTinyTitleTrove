import os

# Define a base directory


# Use os.path.join to create a complete file path


#settings
religion= 'hindu'
reqd_entity_labels= ('WORK_OF_ART','PRODUCT','PERSON','ORG','NORP','LOC','LAW','LANGUAGE','GPE','FAC','EVENT')
given_names= ['ame','arthur','Tristan','Kieran']
audio_format= '.wav'

settings= {
    "synsets_off_religions": ['christian']
}

output_folder= os.path.join('data_christian','collected words')+os.sep
# Use the resulting path in your configuration
paths = {
    "collected_words_path": os.path.join(f"data_{religion}",'collected words'),
    "book_directory_for_stories": os.path.join(f'data_{religion}', "book",'story books'),
    "book_directory_for_namebooks": os.path.join(f'data_{religion}', "book",'name books'),
    "complete_dictionary": os.path.join(f'data_{religion}',"results","distance","names.json"),
    "model_names_file": os.path.join(f'data_{religion}','model_names','model_names.json'),
    "model_names_folder": os.path.join(f'data_{religion}','model_names'),
    "save_directory": os.path.join(f'data_{religion}','audio_data','doc_audio_data'),
    "summed_distance_file": os.path.join(f'data_{religion}','results','summed_distance','summed distance.json'),

    "collected_name_audio_data": os.path.join(f'data_{religion}',"audio data","collected name audio data"),
    "given name audio data": os.path.join(f'data_{religion}',"audio data","given name audio data"),
    "summed_distance_file": os.path.join(f'data_{religion}','results','summed_distance','summed distance.json'),
    "distance": os.path.join(f'data_{religion}','results','distance'),
    "summed_distance": os.path.join(f'data_{religion}','results','summed_distance'),
    "person_names": os.path.join(f'data_{religion}','collected words','person_names.json'),
    "individual names": os.path.join(f'data_{religion}','results','distance','each names'),
    "sorted_by_length": os.path.join(f'data_{religion}','results','sorted_by_wordlength')
}
