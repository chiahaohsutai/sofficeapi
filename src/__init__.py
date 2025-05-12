import logging
import logging.config

from dotenv import load_dotenv

load_dotenv()
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,  # Keeps existing loggers like Uvicorn
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "level": "INFO",
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "sofficeapi": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "unoserver": {
                "handlers": ["console"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }
)
