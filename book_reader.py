import spacy
import re
nlp = spacy.load("en_core_web_sm")

class TextProcessor:
    def __init__(self, file_path = r"data\book\krishna volume1.txt"):
        self.file_path = file_path
        self.nlp = spacy.load("en_core_web_sm")

    def read_file(self):
        with open(self.file_path, "r",errors='ignore') as file:
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
        #return self.tokenize_text(splitted_text)


        max_chars_per_string = 50000

        # Split the document into chunks of 50,000 characters or less
        print("splitting book into chunks..")
        book_chunks = [cleaned_text[i:i + max_chars_per_string] for i in range(0, len(cleaned_text), max_chars_per_string)]
        print("tokenising each chunks..")
        doc_of_each_chunk=[self.tokenize_text(each_chunk) for each_chunk in book_chunks]
        return doc_of_each_chunk


if __name__ == "__main__":
    # example usage
    file_path = r"data\book\krishna volume1.txt"
    text_processor = TextProcessor(file_path)
    book_chunked_text = text_processor.process_file()