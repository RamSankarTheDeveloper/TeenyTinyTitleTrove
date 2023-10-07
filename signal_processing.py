import pyttsx3
import os
import librosa
import numpy as np
from fastdtw import fastdtw
from book_reader import WordCollector
import json
import utils
from gtts import gTTS 
import create_dictionary_match
import config





class main():

    def save_modelnames_in_json(self, data= config.given_names, file_path= config.paths["model_names_file"]):
        utils.create_folder_if_not_exists(config.paths["model_names_folder"])
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)

    def make_folders_if_not(self):
        utils.create_folder_if_not_exists(config.paths["given name audio data"])
        utils.create_folder_if_not_exists(config.paths["collected_name_audio_data"])
        utils.create_folder_if_not_exists(config.paths['distance'])   
        utils.create_folder_if_not_exists(config.paths['summed_distance'])
        self.save_modelnames_in_json(config.given_names)

    def collect_saved_names(self):
        self.given_names_list = utils.extract_data_from_json(config.paths["model_names_file"])
        print("given names count in list= ",self.given_names_list)
        self.collected_names_list = utils.extract_data_from_json(config.paths["person_names"])
        print("collected names count in list= ",self.collected_names_list)
        #word_comparer = utils.WordsComparer()
    
    def get_and_filter_name_data(self):
        self.given_names_list = utils.extract_data_from_json(config.paths["model_names_file"])
        print("given names count in list= ",self.given_names_list)
        self.collected_names_list = utils.extract_data_from_json(config.paths["person_names"])
        print("collected names count in list= ",self.collected_names_list)



    def audio_saver(self): #remove dependency on self to be standalone
        def checkandfilter_ifitin_audiolist(data_list):
            data_list= [word for word in data_list if word not in [file.replace(f"{config.audio_format}",'') for _, _, files in os.walk(config.paths["collected_name_audio_data"]) for file in files]]
            print("datalist=",len(data_list))
            return data_list
        
                        #inner list is audio_file_names
                        
        for each_given_name in self.given_names_list:
            try:
                utils.AudioConverter(word= each_given_name, engine= 'pyttsx3', save_directory=config.paths["given name audio data"]).process()
            except:
                print(f"failed to save {each_given_name}")
                os.remove(os.join.path(config.paths["given name audio data"],os.sep,f'{each_given_name}{config.audio_format}'))
        for each_collected_name in checkandfilter_ifitin_audiolist(self.collected_names_list):
            try:
                utils.AudioConverter(word= each_collected_name, engine= 'pyttsx3', save_directory=config.paths['collected_name_audio_data']).process()
            except:
                print(f"failed to save {each_collected_name}")
                os.remove(os.join.path(config.paths["collected_name_audio_data"],os.sep,f'{each_collected_name}{config.audio_format}'))

    def create_comparison_dictionary(self):
        output_dict = {}
        print("comparing..")
        for each_givenname_audio_filepath in utils.return_each_files_path(subfolder_path= config.paths['given name audio data']):#make a an object of this function with intent specified. the intent is to get given names from the audio folders sincve there could be losses in between the list of names and audio saves
            each_givenname = each_givenname_audio_filepath.replace(f"{config.audio_format}", "")
            each_givenname = each_givenname.replace(config.paths["given name audio data"]+os.sep, "")           
            output_dict[each_givenname] = {}  # Initialize an empty dictionary for each given name
            for each_collectedname_audio_filepath in utils.return_each_files_path(subfolder_path= config.paths['collected_name_audio_data']):
                each_collectedname = each_collectedname_audio_filepath.replace(f"{config.audio_format}", "")
                each_collectedname = each_collectedname.replace(config.paths["collected_name_audio_data"]+os.sep, "")
                print(each_givenname,' is comparing with ',each_collectedname)

                comparison_value = utils.WordsComparer(each_givenname_audio_filepath, each_collectedname_audio_filepath).process()
                output_dict[each_givenname][each_collectedname] = comparison_value         
        #print(output_dict)

        #utils.save_as_json(data=output_dict,file_name='names',subdirectory=os.path.join('data_christian','results','distance'))
        with open(config.paths['complete_dictionary'], 'w') as json_file:
            json.dump(output_dict, json_file)
            print('match updated in names.json')
        return output_dict

    def preprocess_comparison_dict(self,output_dict):

        def normalise_dict(dict):
            decimal_point_for_factor= len(dict.values())/10 #make sure the count of names is above 10 for intuitive understanding
            factor= decimal_point_for_factor/sum(dict.values())
            print("refactoring and standardising matches..")
            for k in dict:
                dict[k] = dict[k]*factor
            return dict
        
        for key, inner_dict in output_dict.items(): #normalise each dict_values for summation
            output_dict[key] = normalise_dict(inner_dict)

        with open(config.paths['complete_dictionary'], 'w') as json_file:
            json.dump(output_dict, json_file)

        #sum of dict
        sum_dict = {}
        print('averaging matches..')
        # Iterate through the original dictionary
        for outer_key, inner_dict in output_dict.items():
            for inner_key, inner_value in inner_dict.items():
                # Check if the inner key is already in sum_dict
                if inner_key in sum_dict:
                    sum_dict[inner_key] = sum_dict[inner_key] + inner_value
                else:
                    sum_dict[inner_key] = inner_value
        print('sorting..')
        sorted_dict = dict(sorted(sum_dict.items(), key=lambda item: item[1]))
        #utils.save_as_json(data=sum_dict,file_name='names',subdirectory=os.path.join('data_christian','results','summed_distance'))
        print('names= ',[name for name in output_dict.keys()], "words= ", len(sorted_dict.values()), "sum= ", sum(sorted_dict.values()))
        print('output= ', sorted_dict)
        with open(config.paths["summed_distance_file"], 'w') as json_file:
            json.dump(sorted_dict, json_file)


    
    def process(self):
        self.save_modelnames_in_json()
        self.make_folders_if_not()
        self.collect_saved_names()
        self.audio_saver()
        output_dict = self.create_comparison_dictionary()
        output_dict = create_dictionary_match.compare_audio_files(config.paths["given name audio data"], config.paths["collected_name_audio_data"])
        self.preprocess_comparison_dict(output_dict=output_dict)



if __name__ == "__main__" :
    main().process()
    # make a code to make folder names

