import os
import shutil
import zipfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader



TEMPLATE_DIR = Path(__file__).parent / "templates"
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
env.globals['enumerate'] = enumerate
env.trim_blocks = True
env.lstrip_blocks = True


def create_epub_structure(base_dir):
	if base_dir.is_dir():
		shutil.rmtree(base_dir)

	(base_dir / "META-INF").mkdir(parents=True, exist_ok=True)
	(base_dir / "OEBPS").mkdir(exist_ok=True)

	# mimetype file
	with open(base_dir / "mimetype", "w", encoding="utf-8") as f:
		f.write("application/epub+zip")

	# container.xml
	with open('static/container.xml') as f:
		container_xml = f.read()

	with open(base_dir / "META-INF" / "container.xml", "w", encoding="utf-8") as f:
		f.write(container_xml)


def render_template(name, **kwargs):
	return env.get_template(name).render(**kwargs)


def create_epub_from_book(book, epub_filepath="epubs/froot.epub", title="The Book of Froot", author="John Smith"):
	temp_dir = Path("temp_epub")
	create_epub_structure(temp_dir)
	oebps_dir = temp_dir / "OEBPS"
	(oebps_dir / "texts").mkdir(exist_ok=True)

	for i, chapter in enumerate(book.chapters):
		chapter_content = render_template("chapter.xhtml.j2", chapter=chapter)
		with open(oebps_dir / chapter.output_filepath, "w", encoding="utf-8") as f:
			f.write(chapter_content)

	# Add inline toc
	content_opf = render_template(
		"inline_toc.xhtml.j2",
		page_title="Table of Contents",
		book=book
	)
	with open(oebps_dir / "inline_toc.xhtml", "w", encoding="utf-8") as f:
		f.write(content_opf)

	# Write OPF
	content_opf = render_template(
		"content.opf.j2",
		title=title,
		book=book,
		author=author
	)
	with open(oebps_dir / "content.opf", "w", encoding="utf-8") as f:
		f.write(content_opf)

	# Write NCX
	toc_ncx = render_template(
		"toc.ncx.j2",
		title=title,
		book=book
	)
	with open(oebps_dir / "toc.ncx", "w", encoding="utf-8") as f:
		f.write(toc_ncx)

	# Create EPUB zip
	with zipfile.ZipFile(epub_filepath, "w") as epub:
		epub.write(temp_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
		for root, _, files in os.walk(temp_dir):
			for file in files:
				if file == "mimetype":
					continue
				full_path = Path(root) / file
				rel_path = full_path.relative_to(temp_dir)
				epub.write(full_path, str(rel_path), compress_type=zipfile.ZIP_DEFLATED)

	shutil.rmtree(temp_dir)
	print(f"EPUB created: {Path(epub_filepath).resolve()} ({len(book.chapters)} chapters)")

