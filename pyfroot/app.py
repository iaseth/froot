from urllib.parse import urljoin

from .args import get_args
from .bookit import FrootBook
from .crawley import Crawley
from .utils import create_uuid



class FrootApp:
	def __init__(self):
		self.args = get_args()
		self.root_url = self.args.url
		self.uuid = create_uuid()
		self.epub_filepath = self.args.output or "epubs/froot.epub"

		self.container_selector = " ".join(self.args.container) if self.args.container else None
		self.items_selector = " ".join(self.args.items) if self.args.items else "a"
		self.link_selector = " ".join(self.args.link) if self.args.link else "a"
		self.article_selector = " ".join(self.args.article)

		self.book = FrootBook(self)
		self.crawler = Crawley([])

	def debug(self, *nargs, **kwargs):
		if self.args.debug:
			print(*nargs, **kwargs)

	def setup_meta_from_page_one(self, soup):
		if self.args.title:
			self.book.title = self.args.title
		else:
			title_tag = soup.find("title")
			if title_tag:
				self.book.title = title_tag.text.strip()

		if self.args.author:
			self.book.author = self.args.author
		else:
			meta_tag = soup.find("meta", attrs={"property": "og:site_name"})
			meta_tag = meta_tag or soup.find("meta", attrs={"name": "twitter:site"})
			if meta_tag:
				self.book.author = meta_tag['content'].strip()

	def download_all_pages(self):
		for page_number in range(self.args.page_start, self.args.page_end + 1):
			self.download_one_page(page_number)

		urls = [ch.full_url for ch in self.book.chapters]
		self.crawler.add_urls(urls)
		self.crawler.download()

	def download_one_page(self, page_number):
		if page_number == 1:
			page_url = self.root_url
		else:
			page_url = "/".join([self.root_url, "page", str(page_number)])

		print(f"Downloading {page_url} . . .")
		soup = self.crawler.get_soup(page_url)

		if page_number == 1:
			self.setup_meta_from_page_one(soup)

		body = soup.find("body")
		if self.container_selector:
			container = soup.select_one(self.container_selector)
		else:
			container = body
		items = container.select(self.items_selector)

		if self.args.limit and len(items) > self.args.limit:
			print(f"\t--- Limiting {len(items)} items to {self.args.limit}")
			items = items[:self.args.limit]

		for i, item in enumerate(items, start=1):
			if item.name == 'a':
				a_tag = item
			elif self.link_selector:
				a_tag = item.select_one(self.link_selector)
				if a_tag and a_tag.name != "a":
					a_tag = a_tag.find("a")
			else:
				a_tag = item.find("a")

			if a_tag.has_attr('href'):
				self.book.create_chapter(a_tag)
			# break
		# self.book.print_toc()

	def export_book_as_epub(self):
		if self.book.chapters:
			self.book.export_epub(epub_filepath=self.epub_filepath)
			self.debug(f"\t--- Title: {self.book.title}")
			self.debug(f"\t--- Author: {self.book.author}")
			self.debug(f"\t--- EPUB: {self.epub_filepath}")
		else:
			print(f"\t--- Not found any chapters!")

	def export_book_as_tex(self):
		self.book.export_tex(tex_filepath="temp/froot.tex")

	def get_full_url(self, href):
			return urljoin(self.root_url, href)

	def get_article_content_soup(self, full_url):
		article_soup = self.crawler.get_soup(full_url)
		article_content = article_soup.select_one(self.article_selector)
		return article_content


froot = FrootApp()
