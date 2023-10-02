import os
import numpy as np
import spacy
import re
import json
import pyttsx3 #replace it to librosa
import os
import librosa
import numpy as np
from fastdtw import fastdtw
from gtts import gTTS
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity



def return_each_files_path(subfolder_path, return_type='full path'):
    if return_type == 'full path':
        for root, _, files in os.walk(subfolder_path):
            for file in files:
                yield os.path.join(root, file)
    elif return_type == 'filename':
        for root, _, files in os.walk(subfolder_path):
            for file in files:
                yield file

# Usage example:
# subfolder_path = '/path/to/your/subfolder'
# for path in return_each_files_path(subfolder_path):
#     print(path)

def extract_data_from_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except ValueError as e:
        print(e,"file not found")
    except Exception as e:
        print(f"An error occurred: {e}")

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
        print(f"An error occurred in saving json: {str(e)}")
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
        cleaned_text = re.sub(r'\n', '. ', text)
        #cleaned_text = re.sub(r'[^\n]', '. ', text)
        cleaned_text = re.sub(r'[&]', ' and ', cleaned_text)
        cleaned_text = re.sub(r'[^a-zA-Z.();,?\'\"]', ' ', cleaned_text)
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

class AudioConverter():
    def __init__(self, word, engine, save_directory=['data','audio_data','doc_audio_data']):
        word = word.lower()
        file_path = save_directory+[f"{word}.wav"]
        self.file_path = os.path.join(*file_path)
        self.word = word
        self.engine = engine

    def process(self):
        if self.engine == "gtts":
            try: #consider this as an additional filter for collected names
                tts = gTTS(self.word)
                tts.save(self.file_path)
            except Exception as e:
                print(f"unable to save '{self.word}' due to : {str(e)}")

        elif self.engine == "pyttsx3":#note that this have to be deleted lately because the storage is high(ten times larger than gtts, but quicker and offline)
            file_name = f"{self.word}.wav"
            engine = pyttsx3.init()
            engine.save_to_file(self.word, file_name)
            engine.runAndWait()
        print("sended file path= ", self.file_path)

        return self.file_path
        

class WordsComparer():
    def __init__(self, audio1_path='',audio2_path='') -> None:
        #print("audio path= ", audio1_path)
        self.audio1_path = audio1_path
        self.audio2_path= audio2_path
        #self.file_name = f"{self.word}.wav"
    
    # def convert_to_audio(self, word, engine):

    #     if engine == "gtts":
    #         file_path = os.path.join('data','audio_data','doc_audio_data',f"{word}.wav")
    #         try: #consider this as an additional filter for collected names
    #             tts = gTTS(word)
    #             tts.save(file_path)
    #         except Exception as e:
    #             print(f"unable to save '{word}' due to : {str(e)}")

    #     elif engine == "pyttsx3":#note that this have to be deleted lately because the storage is high(ten times larger than gtts, but quicker and offline)
    #         file_name = f"{word}.wav"
    #         engine = pyttsx3.init()
    #         engine.save_to_file(word, file_name)
    #         engine.runAndWait()

    #     return file_path

    def audio_to_mfcc(self, audio_file_path):

        # Load the audio files #r"data\audio_data\sample_audio_data\output_audio1.wav"
        audio, sr_doc = librosa.load(audio_file_path, sr= 24000)

        # Extract MFCC features
        mfcc_doc = librosa.feature.mfcc(y= audio, sr= sr_doc)

        # Transpose MFCCs for compatibility with DTW
        mfcc_doc = mfcc_doc.T
        return mfcc_doc


    def compare_two_MFCC(self, mfcc1, mfcc2):
        # Normalize the MFCCs
        scaler = StandardScaler()
        mfcc1_normalized = scaler.fit_transform(mfcc1)
        mfcc2_normalized = scaler.transform(mfcc2)

        # Calculate the cosine similarity between the normalized MFCCs
        similarity = cosine_similarity(mfcc1_normalized, mfcc2_normalized)

        # Scale the similarity to the range 0-100
        scaled_distance = (1 - similarity) * 100

        # Calculate the mean similarity score
        mean_similarity = np.mean(scaled_distance)

        # Adjust the mean similarity score based on the lengths of the MFCCs
        length_difference = abs(len(mfcc1) - len(mfcc2))
        adjusted_similarity = mean_similarity + length_difference

        # Round the adjusted similarity to the nearest integer
        rounded_adjusted_similarity = int(round(adjusted_similarity))

        return rounded_adjusted_similarity

        #return scaled_distance
        #return distance

        #dtw removed due to sensitive to lenght of names
        # def calculate_distance(mfcc1,mfcc2):
        #     if mfcc1.shape[1] != mfcc2.shape[1]:
        #         raise ValueError("Number of features (columns) must be the same for both sequences")

        #         # Calculate the DTW distance using the fastdtw function
        #     distance, _ = fastdtw(mfcc1, mfcc2)
        #     # Calculate DTW distance and path
  
            #return distance
        

        # distance = calculate_distance(mfcc1,mfcc2)
        # #print(distance)
        # # Normalize the distance (optional)
        # normalised_distance = distance / min(len(mfcc1) , len(mfcc2))
        # normalised_distance = round(normalised_distance,2)

        
        # return normalised_distance

    # def word_to_mfcc(self, word):
    #     audio_converter = AudioConverter(word,'gtts')
    #     file_path = audio_converter.process()
    #     mfcc_file = self.audio_to_mfcc(file_path)
    #     #os.remove(file_name)
    #     return mfcc_file

    def process(self):
        mfcc1 = self.audio_to_mfcc(self.audio1_path)
        mfcc2 = self.audio_to_mfcc(self.audio2_path)


        # mfcc1= self.word_to_mfcc(self.word)
        # mfcc2= self.word_to_mfcc(self.word2)
        distance= self.compare_two_MFCC(mfcc1=mfcc1, mfcc2=mfcc2)
        return distance

if __name__ == "__main__":
    file_path1 = AudioConverter(word='k',engine='gtts').process()
    file_path2 = AudioConverter(word='vanakkam',engine='gtts').process()
    distance = WordsComparer(file_path1,file_path2).process()
    print(distance,file_path2)