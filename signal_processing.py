import pyttsx3 #replace it to librosa
import os
import librosa
import numpy as np
from fastdtw import fastdtw
from book_reader import TextProcessor
import json

class audio_converter():
    def __init__(self, word='',is_sample_name=False) -> None:
        self.word = word.lower()
        self.file_name = f"{self.word}.wav"
        if is_sample_name == True:
            self.destination_path = os.path.join(r"data\audio_data\sample_audio_data", self.file_name)# change to join format for cross platform compatibility
        if is_sample_name == False:
            self.destination_path = os.path.join(r"data\audio_data\doc_audio_data", self.file_name)
        self.convert_to_audio()
        self.move_audiofile_to_subfolder()
        self.load_MFCC()


    def convert_to_audio(self):
        engine = pyttsx3.init()
        engine.save_to_file(self.word, f"{self.word}.wav")
        engine.runAndWait()

    def move_audiofile_to_subfolder(self):
        source_path = self.file_name

        try:
        # Use os.rename to move the file to the subfolder
            os.rename(source_path, self.destination_path)
        except:
            pass

        try:
            os.remove(source_path)
        except:
            pass

    def load_MFCC(self):
        # Load the audio files
        doc_audio_file=self.destination_path
        sample_audio_file=r"data\audio_data\sample_audio_data\output_audio1.wav"
        try:
            doc_audio, sr_doc = librosa.load(doc_audio_file, sr=None)
            sample_audio_file, sr_sample = librosa.load(sample_audio_file, sr=None)

            # Extract MFCC features
            mfcc_doc = librosa.feature.mfcc(y=doc_audio, sr=sr_doc)
            mfcc_sample = librosa.feature.mfcc(y=sample_audio_file, sr=sr_sample)

            # Transpose MFCCs for compatibility with DTW
            mfcc_doc = mfcc_doc.T
            mfcc_sample = mfcc_sample.T

            # Calculate DTW distance and path
            distance, path = fastdtw(mfcc_doc, mfcc_sample)

            # Normalize the distance (optional)
            normalized_distance = distance / min(len(mfcc_sample) , len(mfcc_doc))
            print(normalized_distance)
            return normalized_distance
        except:
            pass





def get_file_paths_in_subfolder(folder_path):
    file_paths = []

    try:
        # List all files in the subfolder
        files = os.listdir(folder_path)

        # Iterate over the files and construct full file paths
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                file_paths.append(file_path)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return file_paths




def clear_subfolder(folder_path):
    try:
        # List all files in the subfolder
        files = os.listdir(folder_path)

        # Iterate over the files and remove each one
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        print(f"Subfolder '{folder_path}' has been cleared.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Usage example:
    path_of_books = os.path.join("data","book")
    file_paths = get_file_paths_in_subfolder(path_of_books)

    # Now, you can loop over the file paths and perform actions on each file

        # Perform actions on the file, such as reading, processing, or deleting


    # Usage example:
    #file_path = r"data\book\krishna volume1.txt"
    list_of_doc = []
    for file_path in file_paths:
        list_of_doc += TextProcessor(file_path).process_file()
    word_distance_dict = {}

    # doc_set = set()
    # for token in doc.ents:
    #     doc_set.update(set(token.text))
    for doc in list_of_doc:
        for word in doc.ents:
            if word.label_ in ('PERSON'):
                try:
                    word_distance_dict[word.text.lower()] = int(audio_converter(word.text).load_MFCC())
                except:
                    pass
        with open('word_dist_dict_all.json', 'w') as json_file:
            json.dump(word_distance_dict, json_file)
            # Specify the file path where you want to save the dictionary as JSON
            #word_distance_dict_path = os.path.join(os.path.join('data','match_details','word_dist_dict_all.json'))
            # Save the dictionary as JSON to the file
            with open('word_dist_dict_all.json', 'w') as json_file:
                json.dump(word_distance_dict, json_file)

        subfolder_path = os.path.join("data","audio_data","doc_audio_data")
        clear_subfolder(subfolder_path)

if __name__ == "__main__" :
    main()
