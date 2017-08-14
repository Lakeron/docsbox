import os
import shutil
import datetime

from pylokit import Office
from wand.image import Image
from tempfile import NamedTemporaryFile, TemporaryDirectory

from rq import get_current_job

from docsbox import app, rq
from docsbox.docs.utils import make_zip_archive, make_thumbnails


def get_num_of_queued_jobs(path):
    """
    Get number of queued jobs
    """
    return 5
