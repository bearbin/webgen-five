import os

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
	os.system("gzip --keep --best --force " + doc)

def postprocess(doc, config, args):
	pass

# Utility Functions

def is_updated(checkPath, againstPath):
	"""
	Check if one file is newer compared to another.

	Arguments:
	checkPath - if True, this file is newer (string)
	againstPath - if False, this file is newer (string)

	Returns True or False
	"""
	if os.path.getmtime(checkPath) > os.path.getmtime(againstPath):
		return True
	else:
		return False
