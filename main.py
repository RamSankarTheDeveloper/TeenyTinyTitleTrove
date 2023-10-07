import book_reader
import signal_processing

'''Make sure the folders and files are in place before executing, since some codes
don't create files, instead only append to the existing files.'''

# Execute the WordCollector from book_reader module
book_reader.WordCollector().process()  # Up to saving audio

# Execute the signal_processing module
signal_processing.Main().process()  # From taking audio
