from .chapter import FrootChapter
from ..utils import create_uuid



class FrootBook:
	def __init__(self, app):
		self.app = app
		self.uuid = create_uuid()
		self.chapters = []

	def create_chapter(self, a_tag):
		chapter = FrootChapter(self, a_tag)
		self.chapters.append(chapter)

	def print_toc(self):
		for i, chapter in enumerate(self.chapters, start=1):
			print(f"{i}. {chapter}")


