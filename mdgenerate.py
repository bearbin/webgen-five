import markdown
import os.path
import codecs
import string
import time

# Configuration
website_name = "The Floaternet"
timeFormula = "%d %B %Y"

# Cache Setup
_cache = {
	"title": {},
}

# Code Start

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

def preprocess(doc, config, args):
	if args.force_generate == True:
		return True
	if (not os.path.isfile(os.path.splitext(doc)[0] + ".htm")) or is_updated(args.template_path, os.path.splitext(doc)[0] + ".htm"):
		return True
	return (not os.path.isfile(os.path.splitext(doc)[0] + ".htm")) or is_updated(doc, os.path.splitext(doc)[0] + ".htm")

def process(doc, config, args):
	print("Converting " + doc + " to HTML.")
	with codecs.open(args.template_path, mode="r", encoding="utf-8") as templateFile:
		template = string.Template(templateFile.read())
	title = get_title(doc)
	head_title = get_head_title(doc)
	canonical = get_canonical(doc, config, args)
	update_time = time.strftime(timeFormula, time.localtime(os.path.getmtime(doc)))
	breadcrumbs = get_breadcrumbs(doc, config, args)
	with codecs.open(doc, mode="r", encoding="utf-8") as markdown_input:
		markdown_generated = markdown.markdown(markdown_input.read())
	html_output = template.substitute(title = title,
	                                  head_title = head_title,
	                                  canonical = canonical,
	                                  update_time = update_time,
	                                  breadcrumbs = breadcrumbs,
	                                  markdown_generated = markdown_generated)
	with codecs.open(doc.replace(".md","")+".htm", mode="w", encoding="utf-8") as f:
		f.write(html_output)
	return True

def postprocess(doc, config, args):
	pass

def finalise(config, args):
	pass

# Utility Functions


def get_canonical(doc, config, args):
	relative_path = os.path.relpath(os.path.splitext(doc)[0], args.chosenPath)
	if os.path.basename(relative_path) == "index":
		relative_path = os.path.dirname(relative_path) + "/"
	return config["baseURL"] + relative_path

def get_breadcrumbs(doc, config, args):
	if is_same_path(doc, os.path.join(args.chosenPath, "index.md")):
		return ""
	breadcrumbs = get_title(doc)
	docdir = os.path.dirname(doc)
	while True:
		titledoc = os.path.join(docdir, "index.md")
		if is_same_path(titledoc, doc):
			docdir = os.path.join(docdir, os.path.pardir)
			continue
		title = get_title(titledoc)
		if is_same_path(args.chosenPath, docdir):
			break
		docdir = os.path.join(docdir, os.path.pardir)
		breadcrumbs = "<a href=\"" + get_canonical(titledoc, config, args) + "\">" + title + "</a> &gt; " + breadcrumbs
	return "<p><a href=\"/\">Home</a> &gt; " + breadcrumbs + "</p>"

 
def get_title(doc):
	try:
		return _cache["title"][doc]
	except KeyError:
		pass
	try:
		with codecs.open(doc + ".title", mode="r", encoding="utf-8") as f:
			_cache["title"][doc] = f.readline().strip()
	except FileNotFoundError:
		_cache["title"][doc] = website_name
	return _cache["title"][doc]

def get_head_title(doc):
	title = get_title(doc)
	if title != website_name:
		return title + " &middot; " + website_name
	else:
		return title

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
