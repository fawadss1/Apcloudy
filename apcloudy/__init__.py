"""
APCloudy Client - Distributed Web Scraping as a Service
"""

from .http_client import APCloudyClient
from .config import config
from .models import Job, JobState, Spider, Project
from .exceptions import (
    APCloudyException, APIError, AuthenticationError, JobNotFoundError,
    ProjectNotFoundError, SpiderNotFoundError, RateLimitError
)
from .utils import chunk_urls

__version__ = "0.1.0"
__author__ = "Fawad Ali"
__email__ = "fawadstar@gmail.com"

__all__ = [
    "APCloudyClient",
    "config",
    "Job",
    "JobState",
    "Spider",
    "Project",
    "APCloudyException",
    "APIError",
    "AuthenticationError",
    "JobNotFoundError",
    "ProjectNotFoundError",
    "SpiderNotFoundError",
    "RateLimitError",
    "chunk_urls"
]
