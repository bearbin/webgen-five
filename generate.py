#!/usr/local/bin/python

# Imports

import argparse
import codecs
from functions import find_files
import markdown
import os.path

# Generators

import contentpages
import sitemapgenerate
import tagpages

def extract_wg5(file_path):
	"""
	Extract wg5 data from a file.

	Arguments:
	file_path - the path to the file from which data is to be extracted

	Returns a dictionary containing:

	content - the markdown-converted contents of the file
	metadata - metadata from the file
	mod_time - time of last modification
	"""
	data = {}
	data["mod_time"] = os.path.getmtime(file_path)
	with codecs.open(file_path, mode="r", encoding="utf-8") as f:
		md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
		data["content"] = md.convert(f.read())
		data["metadata"] = md.Meta
	return data

# Register the command line options.

parser = argparse.ArgumentParser(description="webgen-five static site generator.")
parser.add_argument("--input", dest="input_path", help="path to operate on (default '.')", default=".")
parser.add_argument("--output", dest="output_path", help="path for output to be stored in (default './out')", default="./out")
parser.add_argument("--config-path", dest="config_path", help="path for config information (default ''./wgconfig.py')", default="./wgconfig.py")
for generator in (contentpages,tagpages,sitemapgenerate):
	for arg in generator.arguments:
		parser.add_argument(arg["name"], dest=arg["dest"], action=arg["method"], help=arg["help"], default=arg["default"])
args = parser.parse_args()

# Parse the configuration

with open(args.config_path) as f:
    code = compile(f.read(), args.config_path, 'exec')
    exec(code)

# Find documents to operate on in input directory.

documents = find_files(args.input_path, (".wg5",))

# Extract metadata and build list of documents.

md_documents = [dict({"path": doc}.items() + extract_wg5(doc).items()) for doc in documents]

# Build content pages.

for document in md_documents:
	contentpages.generate(document, configuration, args)

# Build tag index.

tags = {}
for document in md_documents:
	for tag in document["metadata"]["tags"]:
		tags.setdefault(tag, []).append(document)

# Build tag pages.

for key in tags:
	tagpages.generate(key, tags[key], configuration, args)

# Generate sitemap.

sitemapgenerate.generate(configuration, args)
