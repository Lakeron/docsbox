import os

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 0

RQ_POLL_INTERVAL = 2500  #: Web interface poll period for updates in ms
DEBUG = False
