import codecs
import markdown
import os.path
import pystache
import string
import time
from functions import get_canonical, get_basename

# Configuration
time_formula = "%d %B %Y"

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

def generate(doc, config, args):
	out_file = os.path.join(args.output_path, get_basename(doc)) + ".htm"
	print("writing " + out_file)
	with codecs.open(args.template_path, mode="r", encoding="utf-8") as template_file:
		template = template_file.read()
	html_output = pystache.render(template, {
		"ads_enabled": (doc["metadata"]["ads"][0].lower() in ("yes", "true", "t", "1")),
		"canonical": get_canonical(doc, config),
		"description": doc["metadata"]["description"][0],
		"content": doc["content"],
		"tags": get_tags(doc),
		"meta_enabled": (get_tags(doc) != []),
		"title": doc["metadata"]["title"][0],
		"update_time": time.strftime(time_formula, time.localtime(doc["mod_time"])),
		"website_name": config["website_name"]
	})
	with codecs.open(out_file, mode="w", encoding="utf-8") as f:
		f.write(html_output)
	return True

# Utility Functions

def get_tags(doc):
	if (doc["metadata"]["tags"] == ['']) or (get_basename(doc) == "index"):
		return []
	return [{"tag": i} for i in sorted(doc["metadata"]["tags"])]
