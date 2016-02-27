import os.path
import time
from functions import find_files

# Configuration
_change_frequency = "weekly"

# Sitemaps need no arguments.
arguments = []

def generate(config, args):
	# Find files to be included in the sitemap.
	files = find_files(args.output_path, (".htm", ".html"))
	sitemap = [
		"<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
		,"<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
	]
	for file in files:
		canonical_url = config["base_url"] + os.path.relpath(file, os.path.splitext(args.output_path)[0])
		# Get file modification time.
		formatted_time = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(file)))
		# Squidge the data onto the array.
		sitemap.append("  <url>")
		sitemap.append("    <loc>" + canonical_url + "</loc>")
		sitemap.append("    <lastmod>" + formatted_time + "</lastmod>")
		sitemap.append("    <changefreq>" + _change_frequency + "</changefreq>")
		sitemap.append("  </url>")
	sitemap.append("</urlset>")
	print("Writing sitemap!")
	with open(os.path.join(args.output_path, "sitemap.xml"), "w") as sm:
		sm.write("\n".join(sitemap))
