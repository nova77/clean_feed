# import sys
import requests

from dateutil import parser
from typing import Optional

import feedparser
import pytz

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

  published = parser.parse(entry_dict['published'])  # type: ignore
  published = published.replace(tzinfo=pytz.timezone('Europe/Zurich'))
  entry.published(published)
  return entry


def _init_feed(feed_url, feed_dict) -> FeedGenerator:
  new_feed = FeedGenerator()
  new_feed.id(feed_url)
  new_feed.title(feed_dict['title'])
  new_feed.link(href=feed_dict['link'])
  new_feed.description(feed_dict['description'])
  new_feed.language(feed_dict['language'])
  return new_feed


def clean_and_merge_feeds(feed_urls) -> Optional[FeedGenerator]:
  new_feed = None
  entries = []
  for feed_url in feed_urls:
    feed_dict = _fetch_and_parse(feed_url)
    if new_feed is None:
      new_feed = _init_feed(feed_url, feed_dict['feed'])
    for entry_dict in feed_dict['entries']:
      entries.append(_create_feed_entry(entry_dict))
  # sort by published date: newest first
  entries.sort(key=lambda entry: entry.published(), reverse=True)
  for entry in entries:
    new_feed.add_entry(entry, order='append')
  return new_feed
