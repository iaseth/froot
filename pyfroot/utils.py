import os
import uuid

import requests
from bs4 import BeautifulSoup



session = requests.session()


def create_uuid():
	return str(uuid.uuid4())

def get_page(url: str):
	response = session.get(url)
	return response

def get_soup(whatever: str):
	if os.path.isfile(whatever):
		with open(whatever) as f:
			soup = BeautifulSoup(f.read(), "lxml")
	else:
		response = get_page(whatever)
		soup = BeautifulSoup(response.text, "lxml")
	return soup

