import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import config

nltk.download("stopwords")
nltk.download("wordnet")

def remove_english_from_list( list_data):
    def has_synonyms(word):
        # Get WordNet synsets for the word
        synsets = wordnet.synsets(word)
        # If there are multiple synsets, it has synonyms
        print(synsets)
        return len(synsets) > 1
    if config.religion not in config.settings['synsets_off_religions']:
        list_data = [word for word in list_data if not has_synonyms(word)]
    stop_words = set(stopwords.words('english'))
    list_data = [word for word in list_data if not word in stop_words]
    return list_data
