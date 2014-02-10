import os
import gzip

# Defenitions

arguments = []

extensions = [
	".css"
	,".htm"
	,".html"
	,".js"
]

# Code Start

def preprocess(doc, config, args):
	if args.force_generate:
		return True
	return (not os.path.isfile(doc + ".gz") or is_updated(doc, doc + ".gz"))

def process(doc, config, args):
	print("Compressing: " + doc)
	gzip_file(doc)

def postprocess(doc, config, args):
	pass

# Utility Functions

def gzip_file(doc):
	with open(doc, "rb") as in_file:
		with gzip.open(doc + ".gz", "wb") as out_file:
			out_file.writelines(in_file)

def is_updated(checkPath, againstPath):
	"""
	Check if one file is newer compared to another.

	Arguments:
	checkPath - if True, this file is newer (string)
	againstPath - if False, this file is newer (string)

	Returns True or False
	"""
	return os.path.getmtime(checkPath) > os.path.getmtime(againstPath)
