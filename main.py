
import book_reader
import signal_processing

'''make sure the folders and files are inplace before executing, since some codes
 doesn't create files, instead only append to the existing files.'''

#signal_processing.save_modelnames_in_json(['vrindh','levik','sandeep','lakshmi','sanvik'])
book_reader.WordCollector().process()#upto saving audio
signal_processing.main().process()#from taking audio