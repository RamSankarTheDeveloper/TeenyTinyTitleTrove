
import book_reader
import signal_processing

'''make sure the folders and files are inplace before executing, since some codes
 doesn't create files, instead only append to the existing files.'''
book_reader.WordCollector().process()
signal_processing.main().process()