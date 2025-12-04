from ..utils import create_uuid



class FrootChapter:
	def __init__(self, parent, a_tag):
		self.parent = parent
		self.a_tag = a_tag
		self.app = self.parent.app
		self.uuid = create_uuid()

		self.href = self.a_tag['href']
		self.title = self.a_tag.text.strip()
		self.full_url = self.app.get_full_url(self.href)

	@property
	def output_filepath(self):
		return f"texts/{self.uuid}.html"

	def get_content(self):
		return "Foo is a Faa."

	def __str__(self):
		return f"Chapter - {self.title} ({self.href})"


