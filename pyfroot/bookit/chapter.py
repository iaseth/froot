


class FrootChapter:
	def __init__(self, parent, a_tag):
		self.parent = parent
		self.a_tag = a_tag
		self.app = self.parent.app

		self.href = self.a_tag['href']
		self.title = self.a_tag.text.strip()
		self.full_url = self.app.get_full_url(self.href)

	def __str__(self):
		return f"Chapter - {self.title} ({self.href})"


