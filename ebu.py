#!/usr/bin/env python3
import argparse

from pyebu.utils import get_soup



def get_args():
	parser = argparse.ArgumentParser()

	parser.add_argument("url", help="The main URL of the blog")
	parser.add_argument("-c", "--container", nargs="+", metavar="SELECTOR", help="CSS selectors for listings container")
	parser.add_argument("-i", "--items", nargs="+", metavar="SELECTOR", help="CSS selectors for listing items")
	parser.add_argument("-l", "--link", nargs="+", metavar="SELECTOR", help="CSS selectors for listing item link")
	parser.add_argument("-a", "--article", nargs="+", metavar="SELECTOR", help="CSS selectors for article content")

	parser.add_argument("--page-start", type=int, default=1, help="First page number to process")
	parser.add_argument("--page-end", type=int, default=1, help="Last page number to process")

	parser.add_argument("-t", "--title", help="Optional title", default=None)
	parser.add_argument("-d", "--description", help="Optional description", default=None)

	parser.add_argument("--debug", "-z", action='store_true', help="Turn on debug mode", default=False)

	return parser.parse_args()


def main():
	args = get_args()
	def debug(*nargs, **kwargs):
		if args.debug:
			print(nargs, kwargs)

	debug(args)
	soup = get_soup(args.url)

	container_selector = " ".join(args.container)
	container = soup.select_one(container_selector)

	items_selector = " ".join(args.items) if args.items else "a"
	items = container.select(items_selector)

	for i, item in enumerate(items, start=1):
		if item.name == 'a':
			a = item
		elif args.link:
			selector = " ".join(args.link)
			a = item.select_one(selector)
			if a and a.name != "a":
				a = a.find("a")
		else:
			a = item.find("a")
		print(f"{i}. {a['href']}")
		# break


if __name__ == '__main__':
	main()
