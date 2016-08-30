
def id_from_path(path):
	components = path.split("/")
	candidate = components[len(components) - 2]
	return int(candidate)
