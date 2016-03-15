import markdown
import os.path
import codecs
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
		template = string.Template(template_file.read())
	html_output = template.substitute(
		canonical = get_canonical(doc, config),
		description = doc["metadata"]["description"][0],
		head_title = doc["metadata"]["title"][0] + " &middot; " + config["website_name"],
		html_content = doc["content"],
		tags = get_tags(doc),
		title = doc["metadata"]["title"][0],
		update_time = time.strftime(time_formula, time.localtime(doc["mod_time"]))
	)
	with codecs.open(out_file, mode="w", encoding="utf-8") as f:
		f.write(html_output)
	return True

# Utility Functions

def get_tags(doc):
	if get_basename(doc) == "index":
		return ""
	tags = ["<p>Tagged as: "]
	for tag in sorted(doc["metadata"]["tags"]):
		tags.append("<a href=\"/tag/" + tag + "\">" + tag + "</a>")
	tags.append("</p>")
	return "\n".join(tags)
