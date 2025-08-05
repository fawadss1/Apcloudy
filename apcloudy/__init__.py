"""
A module for interacting with the APCloudy platform.

This module provides functionalities to interact with the APCloudy platform,
including managing configurations, handling jobs and projects, and interacting
with spiders. It also provides utilities for handling HTTP requests and
responses, as well as error handling specific to the platform.

Exports:
- APCloudyClient: A client for making HTTP requests to the APCloudy API.
- config: Configuration handling for the module and application.
- Job: Represents a job in the APCloudy platform.
- JobState: Represents the state of a job in the APCloudy platform.
- Spider: Represents a spider in the APCloudy platform.
- Project: Represents a project in the APCloudy platform.
- Exceptions: APCloudy-specific exceptions for error handling.
- Utilities: Helper functions like `chunk_urls` for processing data.
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
__email__ = "fawadstar6@gmail.com"

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
