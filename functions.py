import os

def find_files(start_path, types=None):
	"""
	Search for files of the type recursively from, starting from `start_path`.

	Arguments:
	start_path - where to start the search for files (string)
	types - what file extensions to search for (tuple)

	Returns a list of relative paths to matched files. (empty list if none found)
	"""
	files = []
	for node in os.listdir(start_path):
		node_path = os.path.join(start_path, node)
		if os.path.isdir(node_path):
			files = files + find_files(node_path, types)
		else:
			if (types == None) or node.endswith(types):
				files.append(node_path)
	return files

def get_basename(doc):
	return os.path.splitext(os.path.basename(doc["path"]))[0]

def get_canonical(doc, config):
	base_name = get_basename(doc)
	if base_name == "index":
		base_name = ""
	return config["base_url"] + base_name
