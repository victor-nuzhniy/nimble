"""Init module for config 'nimble' project."""

from .celeryy import app as celery_app  # noqa

__all__ = ("celery_app",)
