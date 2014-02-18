#!/usr/local/bin/python

# Imports

import argparse
import os.path

# Generators
import mdgenerate
import gzcompress
import sitemapgenerate

# Configuration

enabled_generators = [
	mdgenerate
	,sitemapgenerate
	,gzcompress
]

configuration = {
	# The base URL for the website to be generated.
	"baseURL":      "http://floaternet.com/"
}

# Functions

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

# Register the command line options.

parser = argparse.ArgumentParser(description="Generate a static website from markdown files.")
parser.add_argument("--force", dest="force_generate", action="store_true",
                    help="force generation of site content.")
parser.add_argument("--path", dest="chosenPath", help="choose a path to operate on (default '.')", default=".")
for generator in enabled_generators:
	for arg in generator.arguments:
		parser.add_argument(arg["name"], dest=arg["dest"], action=arg["method"], help=arg["help"], default=arg["default"])
args = parser.parse_args()

# Run the generators.

for generator in enabled_generators:
	documents = findFiles(args.chosenPath)
	generator_mappings = {}
	for extension in generator.extensions:
		generator_mappings[extension] = generator

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

	# Finalisation.
	generator.finalise(configuration, args)
