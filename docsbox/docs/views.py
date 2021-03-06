import ujson
import datetime
import os

from magic import Magic
from tempfile import NamedTemporaryFile

from flask import request
from flask_restful import Resource, abort

from docsbox import app, rq
from docsbox.docs.tasks import remove_file, process_document, test


class DocumentTestView(Resource):

    def get(self):
        args_self = self
        """
        Test
        """
        high_queue = rq.get_queue('high')
        low_queue = rq.get_queue('low')
        default_queue = rq.get_queue('default')

        high_queue.enqueue(test, 5)
        low_queue.enqueue(test, 5)
        return default_queue.enqueue(test, 5)


class DocumentView(Resource):

    def get(self, task_id):
        """
        Returns information about task status.
        """

        for priority in app.config["QUEUES"]:
            queue = rq.get_queue(priority)
            task = queue.fetch_job(task_id)
            if(task):
                break

        if task:
            return {
                "id": task.id,
                "status": task.status,
                "result_url": task.result
            }
        else:
            return abort(404, message="Unknown task_id")


class DocumentCreateView(Resource):

    def post(self):
        """
        Recieves file and options, checks file mimetype,
        validates options and creates converting task
        """
        debug = ''
        if "file" not in request.files:
            return abort(400, message="file field is required")
        else:
            with NamedTemporaryFile(delete=False, prefix=app.config["MEDIA_PATH"]) as tmp_file:
                request.files["file"].save(tmp_file)
                remove_file.schedule(
                    datetime.timedelta(seconds=app.config["ORIGINAL_FILE_TTL"]),
                    tmp_file.name
                )
                with Magic() as magic:  # detect mimetype
                    mimetype = magic.from_file(tmp_file.name)
                    if mimetype not in app.config["SUPPORTED_MIMETYPES"]:
                        return abort(400, message="Not supported mimetype: '{0}'".format(mimetype))

                    # check ext if exist
                    if('ext' in app.config["SUPPORTED_MIMETYPES"][mimetype]):
                        ext_test_filename = request.files["file"].filename
                        ext_test = ext_test_filename.rsplit('.', 1)[1].lower()
                        if(ext_test not in app.config["SUPPORTED_MIMETYPES"][mimetype]['ext']):
                            return abort(400, message="Not supported ext for mimetype {1}: '{0}'".format(ext_test, mimetype))

                options = request.form.get("options", None)
                if options:  # options validation
                    options = ujson.loads(options)
                    formats = options.get("formats", None)
                    if not isinstance(formats, list) or not formats:
                        return abort(400, message="Invalid 'formats' value")
                    else:
                        for fmt in formats:
                            supported = (fmt in app.config["SUPPORTED_MIMETYPES"][mimetype]["formats"])
                            if not supported:
                                message = "'{0}' mimetype can't be converted to '{1}'"
                                return abort(400, message=message.format(mimetype, fmt))
                    thumbnails = options.get("thumbnails", None)
                    if thumbnails:
                        if not isinstance(thumbnails, dict):
                            return abort(400, message="Invalid 'thumbnails' value")
                        else:
                            thumbnails_size = thumbnails.get("size", None)
                            if not isinstance(thumbnails_size, str) or not thumbnails_size:
                                return abort(400, message="Invalid 'size' value")
                            else:
                                try:
                                    (width, height) = map(int, thumbnails_size.split("x"))
                                except ValueError:
                                    return abort(400, message="Invalid 'size' value")
                                else:
                                    options["thumbnails"]["size"] = (width, height)
                else:
                    if mimetype == "application/pdf":
                        options = {
                            "formats": ["html"]
                        }
                    else:
                        options = app.config["DEFAULT_OPTIONS"]

                priority = request.form.get("priority", None)
                if priority in app.config["QUEUES"]:
                    queue = rq.get_queue(priority)
                else:
                    queue = rq.get_queue('default')

                task = queue.enqueue(process_document, tmp_file.name, options, {
                    "mimetype": mimetype,
                })

        return {
            "id": task.id,
            "status": task.status,
            "debug": debug
        }
