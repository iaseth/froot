from urllib.parse import urljoin

from .args import get_args
from .utils import create_uuid, get_soup
from .bookit import FrootBook



class FrootApp:
	def __init__(self):
		self.args = get_args()
		self.root_url = self.args.url
		self.uuid = create_uuid()

		self.container_selector = " ".join(self.args.container)
		self.items_selector = " ".join(self.args.items) if self.args.items else "a"
		self.article_selector = " ".join(self.args.article)
		self.link_selector = " ".join(self.args.link) if self.args.link else "a"

		self.book = FrootBook(self)

	def debug(self, *nargs, **kwargs):
		if self.args.debug:
			print(nargs, kwargs)

	def download(self):
		froot.debug(froot.args)
		soup = get_soup(self.root_url)
		container = soup.select_one(self.container_selector)
		items = container.select(self.items_selector)

		for i, item in enumerate(items, start=1):
			if item.name == 'a':
				a_tag = item
			elif self.link_selector:
				a_tag = item.select_one(self.link_selector)
				if a_tag and a_tag.name != "a":
					a_tag = a_tag.find("a")
			else:
				a_tag = item.find("a")

			self.book.create_chapter(a_tag)
			# article_content = self.get_article_content(full_url)
			# break
		self.book.print_toc()

	def get_full_url(self, href):
			return urljoin(self.root_url, href)

	def get_article_content(self, full_url):
		article_soup = get_soup(full_url)
		article_content = article_soup.select_one(self.article_selector)
		return article_content


froot = FrootApp()
