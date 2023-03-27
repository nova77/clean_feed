from flask import Flask
from flask import request
import clean_and_merge
import logger_config

logger = logger_config.get_logger()

app = Flask(__name__)


@app.route('/')
def base():
  rss_dict = request.args.to_dict(flat=False)
  if not rss_dict or 'rss' not in rss_dict:
    return f'<p>The url should be host:port?rss=my_rss_url&rss=second_rss_url</p>', 404

  feed_urls = rss_dict['rss']
  logger.info(f'Got request for "{feed_urls}". Creating feed.')
  feed_urls = [f'http://{url}' for url in feed_urls]
  fg = clean_and_merge.clean_and_merge_feeds(feed_urls)
  if not fg:
    return '', 404

  xml = fg.atom_str(pretty=True)
  return xml, 200, {'Content-Type': 'text/xml; charset=utf-8'}


@app.route('/favicon.ico')
def no_favicon():
  """Returns 404 if we pass a favicon request."""
  return '', 404
