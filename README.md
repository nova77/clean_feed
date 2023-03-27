# A simple python app which "cleans" and merge rss feeds

## Standalone binary

To run as a standalone binary, just do:

```bash
pip install -r requirements.txt
python clean_and_merge.py http://first_rss http://second_rss [...]
```

## Docker

You can run it as a HTTP service either locally or as a docker.
To run locally, just do:

```bash
pip install -r requirements.txt
FLASK_APP=app/main.py flask run
```

Then test it on `http://127.0.0.1:5000?rss=url_of_rss_feed`.

Here's the docker compose configuration:

```docker
version: '3'

services:
  clean-feed:
    build: https://github.com/nova77/clean_feed.git
    container_name: clean-feed
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - 5000:5000
```
