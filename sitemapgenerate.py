import os.path
import time

# Configuration
_change_frequency = "daily"

# Code Start

arguments = []

extensions = [
	".htm"
	,".html"
]

# Define the global sitemap.
_sitemap = [
	"<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
	,"<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
]

def preprocess(doc, config, args):
	return True

def process(doc, config, args):
	# Get the canonical URL for the file.
	canonical_url = get_canonical(doc, config, args)
	# Get file modification time.
	modification_time = os.path.getmtime(doc)
	formatted_time = time.strftime("%Y-%m-%d", time.localtime(modification_time))
	# Squidge the data onto the array.
	_sitemap.append("  <url>")
	_sitemap.append("    <loc>" + canonical_url + "</loc>")
	_sitemap.append("    <lastmod>" + formatted_time + "</lastmod>")
	_sitemap.append("    <changefreq>" + _change_frequency + "</changefreq>")
	_sitemap.append("  </url>")

def postprocess(doc, config, args):
	pass

def finalise(config, args):
	print("Writing sitemap!")
	_sitemap.append("</urlset>")
	with open(os.path.join(args.chosenPath, "sitemap.xml"), "w") as sm:
		sm.write("\n".join(_sitemap))

# Utility Functions

def get_canonical(doc, config, args):
        relative_path = os.path.relpath(os.path.splitext(doc)[0], args.chosenPath)
        if os.path.basename(relative_path) == "index":
                relative_path = os.path.dirname(relative_path) + "/"
        return config["baseURL"] + relative_path
