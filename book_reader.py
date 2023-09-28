import spacy
import re

class TextProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nlp = spacy.load("en_core_web_sm")

    def read_file(self):
        with open(self.file_path, "r") as file:
            file_contents = file.read()
        return file_contents

    def clean_text(self, text):
        cleaned_text = re.sub(r'[^a-zA-Z\s.()\'\";,?]', '', text)
        cleaned_text = re.sub(r'[&]', 'and', cleaned_text)
        return cleaned_text

    def tokenize_text(self, text):
        doc = self.nlp(text)
        return doc

    def process_file(self):
        file_contents = self.read_file()
        cleaned_text = self.clean_text(file_contents)
        splitted_text = cleaned_text[:50000]
        return self.tokenize_text(splitted_text)


if __name__ == "__main__":
    # example usage
    file_path = r"data\book\krishna volume1.txt"
    text_processor = TextProcessor(file_path)
    doc = text_processor.process_file()

    for i in doc.sents:
        print('*'*50)
        print(i)