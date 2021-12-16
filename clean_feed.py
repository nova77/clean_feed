# Clean XML feed(s).
# Usage:
#  python clean_feed.py feed_url [feed_url ...]

import sys
import requests

import datetime
from dateutil import parser

import feedparser
from feedgen.entry import FeedEntry
from feedgen.feed import FeedGenerator


def _fetch_and_parse(url) -> feedparser.FeedParserDict:
  r = requests.get(url)
  return feedparser.parse(r.text)


def _create_feed_entry(entry_dict: feedparser.FeedParserDict) -> FeedEntry:
  entry = FeedEntry()
  entry.id(entry_dict['id'])
  entry.title(entry_dict['title'])
  entry.link(href=entry_dict['link'])
  entry.summary(entry_dict['summary'])

  published = parser.parse(entry_dict['published'])
  published = published.replace(tzinfo=datetime.timezone.utc)
  entry.published(published)

  return entry


def init_feed(feed_dict):
  new_feed = FeedGenerator()
  new_feed.title(feed_dict['title'])
  new_feed.link(href=feed_dict['link'])
  new_feed.description(feed_dict['description'])
  new_feed.language(feed_dict['language'])
  return new_feed


def fetch_clean_save(feed_urls):
  new_feed = None
  for feed_url in feed_urls:
    feed_dict = _fetch_and_parse(feed_url)
    if new_feed is None:
      new_feed = init_feed(feed_dict['feed'])
    for entry_dict in feed_dict['entries']:
      new_feed.add_entry(_create_feed_entry(entry_dict))

  print(new_feed.rss_str(pretty=True).decode('utf-8'))


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: clean_feed.py feed_url [feed_url ...]")
  else:
    fetch_clean_save(sys.argv[1:])
