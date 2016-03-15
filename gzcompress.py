import os
import gzip

# Defenitions

# gzip compression needs no arguments
arguments = []

# Code Start

def generate(doc):
	print("Compressing: " + doc)
	gzip_file(doc)

# Utility Functions

def gzip_file(doc):
	with open(doc, "rb") as in_file:
		with gzip.open(doc + ".gz", "wb") as out_file:
			out_file.writelines(in_file)
