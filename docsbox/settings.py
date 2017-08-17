import os

# Queues to listen on
QUEUES = ['high', 'low', 'default']


# RQ DASHBOARD
RQ_POLL_INTERVAL = 1000  #: Web interface poll period for updates in ms


REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
RQ_REDIS_URL = REDIS_URL


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA_PATH = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"


SUPPORTED_FORMATS = {
    "pdf": {
        "path": "pdf",
        "fmt": "pdf",
    },
    "txt": {
        "path": "txt",
        "fmt": "txt",
    },
    "html": {
        "path": "html",
        "fmt": "html",
    },
    "csv": {
        "path": "csv",
        "fmt": "csv",
    }
}


DOCUMENT_EXPORT_FORMATS = ["pdf", "txt", "html"]
SPREADSHEET_EXPORT_FORMATS = ["pdf", "csv", "html"]
PRESENTATION_EXPORT_FORMATS = ["pdf", "html"]
PDF_EXPORT_FORMATS = ["html"]


SUPPORTED_MIMETYPES = {

    # doc as zipped xml
    "application/zip": {
        "formats": DOCUMENT_EXPORT_FORMATS,
        "ext": ["doc", "docx"],
    },

    # doc as html
    "text/html": {
        "formats": DOCUMENT_EXPORT_FORMATS,
        "ext": ["doc", "docx"],
    },

    # doc as x-empty
    "inode/x-empty": {
        "formats": DOCUMENT_EXPORT_FORMATS,
        "ext": ["doc", "docx"],
    },

    # doc as steam documents
    "application/octet-stream": {
        "formats": DOCUMENT_EXPORT_FORMATS,
        "ext": ["doc", "docx"],
    },

    # doc as CDFV2-unknown
    "application/CDFV2-unknown": {
        "formats": DOCUMENT_EXPORT_FORMATS,
    },

    # doc as CDFV2
    "application/CDFV2": {
        "formats": DOCUMENT_EXPORT_FORMATS,
    },

    # Microsoft Word 2003
    "application/msword": {
        "formats": DOCUMENT_EXPORT_FORMATS,
    },

    # Microsoft Word 2007
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        "formats": DOCUMENT_EXPORT_FORMATS,
    },

    # LibreOffice Writer
    "application/vnd.oasis.opendocument.text": {
        "formats": DOCUMENT_EXPORT_FORMATS,
    },

    # Portable Document Format
    "application/pdf": {
        "formats": PDF_EXPORT_FORMATS,
    },

    # Rich Text Format
    "text/rtf": {
        "formats": DOCUMENT_EXPORT_FORMATS,
    },

    # Microsoft Excel 2003
    "application/vnd.ms-excel": {
        "formats": SPREADSHEET_EXPORT_FORMATS,
    },

    # Microsoft Excel 2007
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
        "formats": SPREADSHEET_EXPORT_FORMATS,
    },

    # LibreOffice Calc
    "application/vnd.oasis.opendocument.spreadsheet": {
        "formats": SPREADSHEET_EXPORT_FORMATS,
    },

    # Microsoft Powerpoint 2003
    "application/vnd.ms-powerpoint": {
        "formats": PRESENTATION_EXPORT_FORMATS,
    },

    # Microsoft Powerpoint 2007
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": {
        "formats": PRESENTATION_EXPORT_FORMATS,
    },

    # LibreOffice Impress
    "application/vnd.oasis.opendocument.presentation": {
        "formats": PRESENTATION_EXPORT_FORMATS,
    },
}


DEFAULT_OPTIONS = {
    "formats": ["pdf"]
}
