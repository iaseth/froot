import requests
from bs4 import BeautifulSoup


session = requests.session()


def get_page(url: str):
	response = session.get(url)
	return response

def get_soup(url: str):
	response = get_page(url)
	soup = BeautifulSoup(response.text, "lxml")
	return soup

