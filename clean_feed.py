# Clean XML feed(s).
# Usage:
#  python clean_feed.py feed_url [feed_url ...]

import sys
import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree


def _read_url_as_xml(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'xml')
  return ElementTree.fromstring(soup.prettify())


def fetch_clean_save(feed_urls):
  merged_feed = None
  for feed_url in feed_urls:
    feed = _read_url_as_xml(feed_url)
    if merged_feed is None:
      merged_feed = feed
    else:
      merged_feed.extend(feed)
  print(ElementTree.tostring(merged_feed, encoding='unicode'))


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: clean_feed.py feed_url [feed_url ...]")
  else:
    fetch_clean_save(sys.argv[1:])
