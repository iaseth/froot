


def minify_html(html: str):
	lines = [line.strip() for line in html.split("\n")]
	lines = [line for line in lines if line]
	html = "".join(lines)
	return html


def minify_soup(soup):
	return minify_html(str(soup))

