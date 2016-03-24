import markdown
import os.path
import codecs
import pystache
import time
from functions import get_canonical, get_basename

# Configuration
time_formula = "%d %B %Y"

# Code Start

# The tag pages need no arguments.
arguments = []

def generate(tag, pages, config, args):
	# Do not create a listing if there are no tags.
	if tag == "":
		return
	out_file = os.path.join(args.output_path, "tag", tag) + ".htm"
	print("writing " + out_file)
	tag_html = ["<ul>"]
	for page in pages:
		tag_html.append("<li><a href=\"" + get_canonical(page, config) + "\">" + page["metadata"]["title"][0] + "</a></li>")
		tag_html.append("</ul>")
	mod_times = [page["mod_time"] for page in pages]
	with codecs.open(args.template_path, mode="r", encoding="utf-8") as template_file:
		template = template_file.read()
	html_output = pystache.render(template, {
		"ads_enabled": False,
		"canonical": config["base_url"] + "tag/" + tag,
		"description": "A list of all pages on " + config["website_name"] + " tagged with " + tag,
		"content": "\n".join(tag_html),
		"tags": [],
		"meta_enabled": False,
		"title": "Pages tagged with " + tag,
		"update_time": time.strftime(time_formula, time.localtime(max(mod_times))),
		"website_name": config["website_name"],
	})
	return True
