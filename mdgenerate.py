import markdown
import os.path
import codecs
import string
import time

# Configuration
website_name = "The Floaternet"
timeFormula = "%d %B %Y"

# Initialisation Information

arguments = [
	{
		"name": "--md-template",
		"dest": "template_path",
		"method": "store",
		"help": "choose a different template (default 'template.htm')",
		"default": "template.htm"
	}
]

extensions = [
	".md",
	".mdown",
	".markdown"
]

requires_meta = True

# Setup

# Tag Pages List
_tags = {}

# Template File
with codecs.open(args.template_path, mode="r", encoding="utf-8") as templateFile:
	template = string.Template(templateFile.read())

# Code Start

def preprocess(doc, config, args, meta):
	if args.force_generate == True:
		return True
	output_path = os.path.splitext(doc)[0] + ".htm"
	if is_updated(os.path.splitext(doc)[0] + ".meta", output_path):
		return True
	if (not os.path.isfile(output_path)) or is_updated(args.template_path, output_path):
		return True
	return is_updated(doc, output_path)

def process(doc, config, args, meta):
	print("Converting " + doc + " to HTML.")
	title = meta["title"]
	head_title = format_head_title(title)
	canonical = get_canonical(doc, config, args)
	update_time = time.strftime(timeFormula, time.localtime(os.path.getmtime(doc)))
	with codecs.open(doc, mode="r", encoding="utf-8") as markdown_input:
		markdown_generated = markdown.markdown(markdown_input.read())
	html_output = template.substitute(title = title,
	                                  head_title = head_title,
	                                  canonical = canonical,
	                                  update_time = update_time,
	                                  markdown_generated = markdown_generated)
	with codecs.open(doc[:-3] + ".htm", mode="w", encoding="utf-8") as f:
		f.write(html_output)
	return True

def postprocess(doc, config, args, meta):
	pass

def finalise(config, args):
	pass

# Utility Functions

def get_canonical(doc, config, args):
	relative_path = os.path.relpath(os.path.splitext(doc)[0], args.chosenPath)
	if os.path.basename(relative_path) == "index":
		relative_path = os.path.dirname(relative_path) + "/"
	if relative_path.endswith("//"):
		relative_path = relative_path[:-1]
	return config["baseURL"] + relative_path

def format_head_title(original_title):
	if original_title != website_name:
		return original_title + " &middot; " + website_name
	else:
		return original_title

def is_updated(checkPath, againstPath):
	"""
	Check if one file is newer compared to another.

	Arguments:
	checkPath - if True, this file is newer (string)
	againstPath - if False, this file is newer (string)

	Returns True or False
	"""
	return os.path.getmtime(checkPath) > os.path.getmtime(againstPath)

def is_same_path(one, two):
	"""
	Check if two paths are the same.

	Arguments:
	one - the first path (string)
	two - the second path (string)

	Returns True or False
	"""
	return os.path.abspath(one) == os.path.abspath(two)
