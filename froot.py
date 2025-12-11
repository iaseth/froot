#!/usr/bin/env python3
from pyfroot import froot



def main():
	froot.download_all_pages()
	froot.export_book_as_epub()
	froot.export_book_as_tex()


if __name__ == '__main__':
	main()
