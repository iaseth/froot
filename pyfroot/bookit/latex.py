import json
import math
import os
from pathlib import Path

import jinja2
from jinja2 import Template

from .latex_formats import formats



def escape(s):
	return s.replace("%", "\\%").replace("$", "\\$").replace("#", "\\#").replace("&", "\\&")


TEMPLATE_DIR = Path(__file__).parent / "templates"

latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(TEMPLATE_DIR)
)

latex_jinja_env.filters['escape'] = escape

master_tex_template = latex_jinja_env.get_template('master.tex')
metadata = json.load(open("metadata.json"))


def create_tex_from_book(book, tex_filepath="froot.tex"):
	tex = master_tex_template.render(
		book=book,
		format=formats[0],
		metadata=metadata
	)
	print(tex)


