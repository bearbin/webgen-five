import markdown
import os.path
import codecs
import string
import time

# Configuration
website_name = "The Floaternet"
timeFormula = "%d %B %Y"

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
	if isUpdated(args.template_path, os.path.splitext(doc)[0] + ".htm"):
		return True
	return (not os.path.isfile(os.path.splitext(doc)[0] + ".htm")) or isUpdated(doc, os.path.splitext(doc)[0] + ".htm")

def process(doc, config, args):
	with codecs.open(args.template_path, mode="r", encoding="utf-8") as templateFile:
		template = string.Template(templateFile.read())
	print("Markdown Converting: " + doc)
	if os.path.exists(doc + ".title"):
		with open(doc + ".title", 'rU') as f:
			for line in f:
				title = line + " &middot; " + website_name
	else:
		title = website_name
	relative_path = (os.path.relpath(os.path.splitext(doc)[0], args.chosenPath) if os.path.relpath(os.path.splitext(doc)[0], args.chosenPath) != "." else "")
	if os.path.split(relative_path)[1] == "index":
		relative_path = os.path.split(relative_path)[0]
	canonical = config["baseURL"] + relative_path
	update_time = time.strftime(timeFormula, time.localtime(os.path.getmtime(doc)))
	with codecs.open(doc, mode="r", encoding="utf-8") as markdown_input:
		markdown_generated = markdown.markdown(markdown_input.read())
	html_output = template.substitute(title = title, canonical = canonical, update_time = update_time, markdown_generated = markdown_generated)
	with codecs.open(doc.replace(".md","")+".htm", mode="w", encoding="utf-8") as f:
		f.write(html_output)

def postprocess(doc, config, args):
	pass

# Utility Functions

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
