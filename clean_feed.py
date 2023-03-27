# Clean XML feed(s).
# Usage:
#  python clean_feed.py feed_url [feed_url ...]

import sys
from app import clean_and_merge


def main(feed_urls):
  fg = clean_and_merge.clean_and_merge_feeds(feed_urls)
  if not fg:
    raise ValueError('Could not find anything')

  print(fg.rss_str(pretty=True).decode('utf-8'))


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: clean_feed.py feed_url [feed_url ...]")
  else:
    main(sys.argv[1:])
