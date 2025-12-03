from urllib.parse import urljoin

from .args import get_args
from .utils import get_soup



class FrootApp:
	def __init__(self):
		self.args = get_args()
		self.root_url = self.args.url

		self.container_selector = " ".join(self.args.container)
		self.items_selector = " ".join(self.args.items) if self.args.items else "a"
		self.article_selector = " ".join(self.args.article)

	def debug(self, *nargs, **kwargs):
		if self.args.debug:
			print(nargs, kwargs)

	def download(self):
		soup = get_soup(self.root_url)
		container = soup.select_one(self.container_selector)
		items = container.select(self.items_selector)

		for i, item in enumerate(items, start=1):
			if item.name == 'a':
				a = item
			elif args.link:
				link_selector = " ".join(self.args.link)
				a = item.select_one(link_selector)
				if a and a.name != "a":
					a = a.find("a")
			else:
				a = item.find("a")

			full_url = self.get_full_url(a['href'])
			print(f"{i}. {full_url}")
			article_content = self.get_article_content(full_url)
			print(article_content)
			break

	def get_full_url(self, href):
			return urljoin(self.root_url, href)

	def get_article_content(self, full_url):
		article_soup = get_soup(full_url)
		article_content = article_soup.select_one(self.article_selector)
		return article_content


froot = FrootApp()
