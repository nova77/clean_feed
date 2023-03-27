from flask import Flask
from flask import request
import clean_and_merge
import logger_config

logger = logger_config.get_logger()

app = Flask(__name__)


@app.route('/')
def base():
  return f'<p>Must pass an url with a feed to parse!</p>'


@app.route('/favicon.ico')
def no_favicon():
  """Returns 404 if we pass a favicon request."""
  return '', 404


@app.route('/<path:url>')
def main_entry(url):
  del url  # Unused since we need full path anyway.
  full_path = request.full_path[1:]  # Strip leading /.
  feed_urls = full_path.split(',')

  logger.info(f'Got request for "{feed_urls}". Creating feed.')
  fg = clean_and_merge.clean_and_merge_feeds(feed_urls)
  if not fg:
    return '', 404

  xml = fg.atom_str(pretty=True)
  return xml, 200, {'Content-Type': 'text/xml; charset=utf-8'}
