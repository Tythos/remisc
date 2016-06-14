"""Interface for package data stored in the "data" folder, providing methods to
   both resolve and load data.
"""

import os

def get_path(data_path):
	"""Returns the absolute path to the indicated data file stored under the
	   'data/' folder co-located with this module.
	"""
	return os.path.dirname(os.path.realpath(__file__)) + os.sep + data_path
	
def get_text(data_path):
	"""Returns the text contents (as a string) of the given file stored under
	   the 'data/' folder co-located with this module.
	"""
	p = get_full_path(data_path)
	f = open(p, 'r')
	content = f.read()
	f.close()
	return content
