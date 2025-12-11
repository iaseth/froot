


def minify_html(html: str):
	lines = [line.strip() for line in html.split("\n")]
	lines = [line for line in lines if line]
	html = "".join(lines)
	return html


def minify_soup(soup):
	return minify_html(str(soup))


def log(message: str, level: int=1, same_line: bool=False):
	prefix = "\t" * level
	if same_line:
		print(f"\r{prefix}--- {message}", end="")
	else:
		print(f"{prefix}--- {message}")

