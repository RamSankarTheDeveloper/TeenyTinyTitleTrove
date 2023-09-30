from book_reader import TextProcessor

file_path = r"data\book\krishna volume1.txt"
text_processor = TextProcessor(file_path)
doc = text_processor.process_file()
doc_set = set()
for token in doc.ents:
    doc_set.update(set(token.text))
