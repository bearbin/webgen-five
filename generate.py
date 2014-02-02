#!/usr/local/bin/python

# Imports

import argparse
import codecs
import string
import time
import os

# Generators
import mdgenerator

# Configuration

enabled_generators = [
	mdgenerator
]

configuration = {
	# The base URL for the website to be generated.
	"baseURL":      "http://floaternet.com/"
	# Static files to be compressed by the gzip-compression routine.
	,"staticFiles": (".css", ".js", ".htm", ".html")
}

# Functions

def compressFiles(files):
	"""
	Compress the listed files, if they were updated since the last compression.

	Arguments:
	files - an iterable with file names to process.
	"""
	for file in files:
		print("Compressing: " + file)
		os.system("gzip --keep --best --force " + file)

def findCompressibleFiles(startPath):
	compressibleFiles = []
	for file in findFiles(startPath, configuration["staticFiles"]):
		if (not os.path.isfile(file + ".gz") or isUpdated(file, file + ".gz")):
			compressibleFiles.append(file)
	return compressibleFiles

def findFiles(startPath, types=None):
	"""
	Search for files of the type recursively from, starting from `startPath`.

	Arguments:
	startPath - where to start the search for files (string)
	types - what file extensions to search for (tuple)

	Returns a list of relative paths to matched files. (empty list if none found)
	"""
	files = []
	for node in os.listdir(startPath):
		nodePath = os.path.join(startPath, node)
		if os.path.isdir(nodePath):
			files = files + findFiles(nodePath, types)
		else:
			if types == None:
				files.append(nodePath)
			elif node.endswith(types):
				files.append(nodePath)
	return files

def isUpdated(checkPath, againstPath):
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

# Register the command line options.
parser = argparse.ArgumentParser(description="Generate a static website from markdown files.")
parser.add_argument("--force", dest="force_generate", action="store_true",
                    help="force generation of site content.")
parser.add_argument("--path", dest="chosenPath", help="choose a path to operate on (default '.')", default=".")
for generator in enabled_generators:
	for arg in generator.arguments:
		parser.add_argument(arg["name"], dest=arg["dest"], action=arg["method"], help=arg["help"], default=arg["default"])
args = parser.parse_args()

# Find generators for file extensions.
generator_mappings = {}

for generator in enabled_generators:
	for extension in generator.extensions:
		generator_mappings[extension] = generator

# Find documents
documents = findFiles(args.chosenPath)

# Preprocess
for doc in documents[:]:
	try:
		keep = generator_mappings[os.path.splitext(doc)[1]].preprocess(doc, configuration, args)
	except KeyError:
		documents.remove(doc)
		continue
	if not keep:
		documents.remove(doc)

# Main Processing
for doc in documents[:]:
	keep = generator_mappings[os.path.splitext(doc)[1]].process(doc, configuration, args)
	if not keep:
		documents.remove(doc) 

# Postprocessing
for doc in documents:
	generator_mappings[os.path.splitext(doc)[1]].preprocess(doc, configuration, args)

# compression
compressibleFiles = findCompressibleFiles(args.chosenPath)
compressFiles(compressibleFiles)
