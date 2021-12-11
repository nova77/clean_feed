# Clean XML feed(s).
# Usage:
#  python clean_feed.py <feed_url>

import sys
import requests
from bs4 import BeautifulSoup


def fetch_clean_save(feed_url):
  r = requests.get(feed_url)
  soup = BeautifulSoup(r.text,'xml') 
  print (soup.prettify()) 


if __name__== "__main__":
  if len(sys.argv) < 2:
    print ("Usage: clean_feed.py feed")
  else:
    fetch_clean_save(sys.argv[1])
