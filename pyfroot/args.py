import argparse



def get_args():
	parser = argparse.ArgumentParser()

	parser.add_argument("url", help="The main URL of the blog")
	parser.add_argument("-c", "--container", nargs="+", metavar="SELECTOR", help="CSS selectors for listings container")
	parser.add_argument("-i", "--items", nargs="+", metavar="SELECTOR", help="CSS selectors for listing items")
	parser.add_argument("-l", "--link", nargs="+", metavar="SELECTOR", help="CSS selectors for listing item link")
	parser.add_argument("-a", "--article", nargs="+", metavar="SELECTOR", help="CSS selectors for article content")

	parser.add_argument("--limit", "-n", type=int, default=0, help="Limit number of chapters")
	parser.add_argument("--page-start", type=int, default=1, help="First page number to process")
	parser.add_argument("--page-end", type=int, default=1, help="Last page number to process")

	parser.add_argument("--author", help="Optional author", default=None)
	parser.add_argument("--title", help="Optional title", default=None)
	parser.add_argument("--description", help="Optional description", default=None)
	parser.add_argument("-o", "--output", help="Optional output filepath", default=None)

	parser.add_argument("--debug", "-z", action='store_true', help="Turn on debug mode", default=False)

	return parser.parse_args()

