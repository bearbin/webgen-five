import markdown
import os.path
import codecs
import string
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
	with codecs.open(args.template_path, mode="r", encoding="utf-8") as template_file:
		template = string.Template(template_file.read())
	tag_html = ["<ul>"]
	for page in pages:
		tag_html.append("<li><a href=\"" + get_canonical(page, config) + "\">" + page["metadata"]["title"][0] + "</a></li>")
	tag_html.append("</ul>")
	mod_times = [page["mod_time"] for page in pages]
	html_output = template.substitute(
		canonical = config["base_url"] + "tag/" + tag,
		description = "A list of all pages tagged with " + tag,
		head_title = tag + " &middot; " + config["website_name"],
		html_content = "\n".join(tag_html),
		tags = "",
		title = "Pages tagged with " + tag,
		update_time = time.strftime(time_formula, time.localtime(max(mod_times)))
	)
	with codecs.open(out_file, mode="w", encoding="utf-8") as f:
		f.write(html_output)
	return True
