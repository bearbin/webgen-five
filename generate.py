#!/usr/local/bin/python

# Imports

import argparse
import os.path
import codecs
import json

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

def find_files(start_path, types=None):
    """
    Search for files of the type recursively from, starting from `startPath`.

    Arguments:
    startPath - where to start the search for files (string)
    types - what file extensions to search for (tuple)

    Returns a list of relative paths to matched files. (empty list if none found)
    """
    files = []
    for node in os.listdir(start_path):
        node_path = os.path.join(start_path, node)
        if os.path.isdir(node_path):
            files = files + find_files(node_path, types)
        elif types == None:
            files.append(node_path)
        elif node.endswith(types):
            files.append(node_path)
    return files

def get_meta(doc):
    """
    Get the meta information relating to a document.
    
    Fetches from the document.meta file.
    """
    with codecs.open(os.path.splitext(doc)[0] + ".meta", encoding="UTF-8") as meta_file:
        return json.loads(meta_file.read())

# Register the command line options.

parser = argparse.ArgumentParser(description="Generate a static website from markdown files.")
parser.add_argument("--force", dest="force_generate", action="store_true",
                    help="force generation of site content.")
parser.add_argument("--path", dest="chosen_path", help="choose a path to operate on (default '.')", default=".")
for generator in enabled_generators:
    for arg in generator.arguments:
        parser.add_argument(arg["name"], dest=arg["dest"], action=arg["method"], help=arg["help"], default=arg["default"])
args = parser.parse_args()

# Run the generators.

for generator in enabled_generators:
    documents = find_files(args.chosen_path)
    generator_mappings = {}
    for extension in generator.extensions:
        generator_mappings[extension] = generator

    # Initialisation
    generator.config = configuration
    generator.args = args
    generator.initialise()

    # Preprocess
    for doc in documents[:]:
        try:
            mapping = generator_mappings[os.path.splitext(doc)[1]]
        except KeyError:
            documents.remove(doc)
            continue
        if mapping.requires_meta:
            meta = get_meta(doc)
        else:
            meta = None
        keep = mapping.preprocess(doc, meta)
        if not keep:
            documents.remove(doc)
    
    # Main Processing
    for doc in documents[:]:
        mapping = generator_mappings[os.path.splitext(doc)[1]]
        if mapping.requires_meta:
            meta = get_meta(doc)
        else:
            meta = None
        keep = mapping.process(doc, meta)
        if not keep:
            documents.remove(doc) 

    # Postprocessing
    for doc in documents:
        mapping = generator_mappings[os.path.splitext(doc)[1]]
        if mapping.requires_meta:
            meta = get_meta(doc)
        else:
            meta = None
        mapping.preprocess(doc, meta)

    # Finalisation.
    generator.finalise()
