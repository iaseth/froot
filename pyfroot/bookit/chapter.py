import os

from ..utils import create_uuid


BAD_TAGS = ["iframe", "img", "audio", "video"]


class FrootChapter:
	def __init__(self, parent, a_tag):
		self.parent = parent
		self.a_tag = a_tag
		self.app = self.parent.app
		self.uuid = create_uuid()

		self.idx = 0
		self.next = None
		self.previous = None

		self.href = self.a_tag['href']
		self.title = self.a_tag.text.strip()
		self.full_url = self.app.get_full_url(self.href)

	@property
	def output_filename(self):
		return f"{self.uuid}.html"

	@property
	def output_filepath(self):
		return os.path.join("texts", self.output_filename)

	def get_content(self):
		soup = self.app.get_article_content_soup(self.full_url)
		if not soup:
			return "No content found!"

		for tag_name in BAD_TAGS:
			for tag in soup.find_all(tag_name):
				tag.decompose()

		for tag in soup.find_all(True):
			tag.attrs = {}

		return soup

	def __str__(self):
		return f"Chapter - {self.title} ({self.href})"


