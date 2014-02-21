import collections.defaultdict
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

config = None
args = None

# Setup

# Tag Pages List
_tag_pages = collections.defaultdict(list)

# Global Template
_template = None

# Code Start

def initialise():
	# Load the template from the specified template file and read it.
	with codecs.open(args.template_path, mode="r", encoding="utf-8") as template_file:
		_template = string.Template(template_file.read())

def preprocess(doc_path, meta):
	if not meta["generate"]:
		return False
	# Add the page to its relevant tag pages.
	for tag in meta["tags"]:
		_tag_pages[tag].append({"subtag": get_subtag(tag), "canonical": get_canonical(doc_path), "title": meta["title"]})
	# If everything is to be generated, generate everything.
	if args.force_generate == True:
		return True
	# Now check to see if it's updated. If it is, then keep it around for updating.
	output_path = os.path.splitext(doc_path)[0] + ".htm"
	if is_updated(os.path.splitext(doc_path)[0] + ".meta", output_path):
		return True
	if (not os.path.isfile(output_path)) or is_updated(args.template_path, output_path):
		return True
	return is_updated(doc_path, output_path)

def process(doc_path, meta):
	print("Converting " + doc_path + " to HTML.")
	# Convert the input markdown into HTML ready for the middle of the template.
	with codecs.open(doc, mode="r", encoding="utf-8") as markdown_input:
		markdown_generated = markdown.markdown(markdown_input.read())
	# Do everything else to the page, and write it to disk.
	generate_document(doc_path, meta, markdown_generated)
	return True

def postprocess(doc_path, meta):
	# Nothing to see here, move along...
	pass

def finalise():
	# First, generate the tag pages from the tags.
	for tag_name, tag_page in _tag_pages:
		generate_tag_page(tag_name, tag_page)
	# Then, generate the main index page.
	generate_index()

# Utility Functions

def generate_tag_page(tag_name, contents):
	tag_path = os.path.join(args.chosen_path, tag_name.split("/", 1)[0], "index")
	meta = get_meta_info(tag_path)
	content = ["<p>", meta["description"], "</p>"]
	subtags = collections.defaultdict{list}
	for doc in contents:
		subtags[doc["subtag"]].append(doc)
	for doc in subtags["main"]:
		pass
	del subtags["main"]
	for subtag, documents in subtags:
		content.append("<h2>" + subtag + "</h2>")
		content.append("<ul>")
		for doc in documents:
			content.append("<li><a href=\"" + doc["canonical"] + "\">" + doc["title"] + "</a></li>")
		content.append("")
	# Generate the tag page.
	generate_document(tag_path, meta, "\n".join(content))


def generate_document(doc_path, meta, content):
	"""
	Generate a document with the information from the meta file, and content to go in the middle.
	"""
	title = meta["title"]
	if meta["plain_title"]:
		head_title = title
	else:
		head_title = title + " &middot; " + website_name
	canonical = get_canonical(doc, config, args)
	description = meta["description"]
	# Generate the timestamp.
	if meta["supress_timestamp"]:
		update_time = ""
	else:
		update_time = time.strftime(timeFormula, time.localtime(os.path.getmtime(doc)))
	html_output = _template.safe_substitute(
		title = title,
	        head_title = head_title,
	        canonical = canonical,
	        description = description,
	        update_time = update_time,
	        content = content
	)
	# Write the generated HTML.
	with codecs.open(os.path.splitext(doc)[0] + ".htm", mode="w", encoding="utf-8") as f:
		f.write(html_output)

def get_meta_info(doc):
	"""
	Get the meta information relating to a document.
	
	Fetches from the document.meta file.
	"""
	with codecs.open(doc + ".meta", encoding="UTF-8") as meta_file:
		return json.loads(meta_file.read())

def get_subtag(tag):
	try:
		return tag.split("/", 1)[1]
	except IndexError:
		return "main"

def get_canonical(doc):
	relative_path = os.path.relpath(os.path.splitext(doc)[0], args.chosen_path)
	if os.path.basename(relative_path) == "index":
		relative_path = os.path.dirname(relative_path) + "/"
	if relative_path.endswith("//"):
		relative_path = relative_path[:-1]
	return config["baseURL"] + relative_path

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
