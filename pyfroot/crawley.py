import os
import asyncio
import aiohttp
import hashlib

from bs4 import BeautifulSoup



BAD_TAGS = ["audio", "video", "script", "style"]


class Crawley:
	def __init__(self, urls, cache_dir=".cache", transform=None):
		"""
		urls: list of URLs to download
		cache_dir: where to store cached HTML files
		transform: optional function(html: str) -> str
		"""
		self.urls = urls
		self.cache_dir = cache_dir
		self.transform = transform

		os.makedirs(cache_dir, exist_ok=True)

	def _hash_url(self, url: str) -> str:
		"""Return SHA-256 hash filename for a URL."""
		return hashlib.sha256(url.encode("utf-8")).hexdigest() + ".html"

	def _cache_path(self, url: str) -> str:
		return os.path.join(self.cache_dir, self._hash_url(url))

	def _is_cached(self, url: str) -> bool:
		return os.path.exists(self._cache_path(url))

	def _read_cache(self, url: str) -> str:
		with open(self._cache_path(url), "r", encoding="utf-8") as f:
			return f.read()

	def _clean_html(self, html: str):
		soup = BeautifulSoup(html, "lxml")
		for tag_name in BAD_TAGS:
			for tag in soup.find_all(tag_name):
				tag.decompose()
		return str(soup)

	def _write_cache(self, url: str, html: str):
		with open(self._cache_path(url), "w", encoding="utf-8") as f:
			f.write(self._clean_html(html))

	async def _fetch(self, session, url: str) -> str:
		"""Fetch a single URL, apply transform, write to cache."""
		async with session.get(url) as resp:
			resp.raise_for_status()
			html = await resp.text()

			if self.transform:
				html = self.transform(html)

			self._write_cache(url, html)
			return html

	async def _download_all(self):
		"""Internal async downloader."""
		urls = [url for url in self.urls if not self._is_cached(url)]
		async with aiohttp.ClientSession() as session:
			tasks = [
				asyncio.create_task(self._fetch(session, url))
				for url in urls
			]
			await asyncio.gather(*tasks)

	def add_urls(self, urls):
		self.urls = [*self.urls, *urls]

	def download(self):
		"""Public sync wrapper to download all URLs."""
		asyncio.run(self._download_all())

	def get(self, url: str) -> str:
		"""
		Return HTML for the URL.
		Prefer cache; if missing, fetch & store.
		"""
		if self._is_cached(url):
			return self._read_cache(url)

		# Not cached → fetch synchronously using asyncio
		async def fetch_one():
			async with aiohttp.ClientSession() as session:
				return await self._fetch(session, url)

		return asyncio.run(fetch_one())

	def get_soup(self, url: str):
		soup = BeautifulSoup(self.get(url), "lxml")
		return soup


