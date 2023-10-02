import pyttsx3
import os
import librosa
import numpy as np
from fastdtw import fastdtw
from book_reader import WordCollector
import json
import utils
from gtts import gTTS 

def save_modelnames_in_json(data):
    utils.save_as_json(data=data,
                        file_name= 'model_names',
                        subdirectory= os.path.join('data','model_names'))
#save_names_in_json()

class main():
    def collect_saved_names(self):
        self.given_names_list = utils.extract_data_from_json(r"data\model_names\model_names.json")
        print("given names count in list= ",self.given_names_list)
        self.collected_names_list = utils.extract_data_from_json(r"data\collected words\person_names.json")
        print("collected names count in list= ",self.collected_names_list)
        #word_comparer = utils.WordsComparer()

    def audio_saver(self): #remove dependency on self to be standalone
        for each_given_name in self.given_names_list:
            utils.AudioConverter(word= each_given_name, engine= 'gtts', save_directory=['data','audio data','given name audio data']).process()
        for each_collected_name in self.collected_names_list:
            utils.AudioConverter(word= each_collected_name, engine= 'gtts', save_directory=['data','audio data','collected name audio data']).process()

    def create_comparison_dictionary(self):
        output_dict = {}
        print("comparing..")
        for each_givenname_audio_filepath in utils.return_each_files_path(subfolder_path=os.path.join("data","audio data","given name audio data")):#make a an object of this function with intent specified. the intent is to get given names from the audio folders sincve there could be losses in between the list of names and audio saves
            each_givenname = each_givenname_audio_filepath.replace('.wav', "")
            each_givenname = each_givenname.replace("data\\audio data\\given name audio data\\", "")
            print(each_givenname)
            output_dict[each_givenname] = {}  # Initialize an empty dictionary for each given name
            for each_collectedname_audio_filepath in utils.return_each_files_path(subfolder_path=os.path.join("data","audio data","collected name audio data")):
                each_collectedname = each_collectedname_audio_filepath.replace('.wav', "")
                each_collectedname = each_collectedname.replace("data\\audio data\\collected name audio data\\", "")
                comparison_value = utils.WordsComparer(each_givenname_audio_filepath, each_collectedname_audio_filepath).process()
                output_dict[each_givenname][each_collectedname] = comparison_value         
        #print(output_dict)

        #utils.save_as_json(data=output_dict,file_name='names',subdirectory=os.path.join('data','results','distance'))
        with open(os.path.join('data','results','distance','names.json'), 'w') as json_file:
            json.dump(output_dict, json_file)
        return output_dict

    def preprocess_comparison_dict(self,output_dict):
        #sum of dict
        sum_dict = {}
        # Iterate through the original dictionary
        for outer_key, inner_dict in output_dict.items():
            for inner_key, inner_value in inner_dict.items():
                # Check if the inner key is already in sum_dict
                if inner_key in sum_dict:
                    sum_dict[inner_key] = int(sum_dict[inner_key] + inner_value)
                else:
                    sum_dict[inner_key] = int(inner_value)

        sorted_dict = dict(sorted(sum_dict.items(), key=lambda item: item[1]))
        #utils.save_as_json(data=sum_dict,file_name='names',subdirectory=os.path.join('data','results','summed_distance'))
        print('output= ', sorted_dict)
        with open(os.path.join('data','results','summed_distance','summed distance.json'), 'w') as json_file:
            json.dump(sorted_dict, json_file)
    
    def process(self):
        self.collect_saved_names()
        self.audio_saver()
        output_dict = self.create_comparison_dictionary()
        self.preprocess_comparison_dict(output_dict=output_dict)



if __name__ == "__main__" :
    #save_modelnames_in_json(['vrindh','levik'])
    
    main().process()
    #make a code to make folder names

