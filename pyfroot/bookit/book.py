from .chapter import FrootChapter
from .epub import create_epub_from_book
from ..utils import create_uuid



class FrootBook:
	def __init__(self, app):
		self.app = app
		self.uuid = create_uuid()
		self.chapters = []
		self.title = "The Book of Froot"
		self.author = "Froot"

	@property
	def length(self):
		return len(self.chapters)

	@property
	def first_chapter(self):
		return self.chapters[0]

	@property
	def last_chapter(self):
		return self.chapters[-1]

	def create_chapter(self, a_tag):
		chapter = FrootChapter(self, a_tag)
		if self.chapters:
			chapter.idx = len(self.chapters)
			chapter.previous = self.last_chapter
			self.last_chapter.next = chapter
		self.chapters.append(chapter)

	def print_toc(self):
		for i, chapter in enumerate(self.chapters, start=1):
			print(f"{i}. {chapter}")

	def export_epub(self):
		create_epub_from_book(self)


