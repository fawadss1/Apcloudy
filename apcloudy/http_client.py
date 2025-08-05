"""
Manages job and spider-related operations for projects in APCloudy.

This module includes classes, `JobsManager` and `SpidersManager`, to perform
operations related to jobs and spiders within specific projects. The operations
include creating, retrieving, listing, canceling, and deleting jobs, as well as
retrieving logs, scraped items, and managing spiders.

Classes:
    JobsManager -- Handles operations for managing jobs within a project.
    SpidersManager -- Handles operations for managing spiders associated with a project.
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any, Iterator, BinaryIO
from urllib.parse import urljoin
from .models import Job, JobState, Spider, Project
from .config import config
from .exceptions import (
    APIError, AuthenticationError, JobNotFoundError,
    ProjectNotFoundError, SpiderNotFoundError, RateLimitError
)


class JobsManager:
    """
    Manages job operations for a project in APCloudy, providing functionalities such as running,
    retrieving, listing, canceling, and deleting jobs, as well as retrieving logs or scraped items.
    It interacts with the APCloudyClient to perform HTTP requests for job-related actions.

    :ivar client: The client instance is used to communicate with the API.
    :type client: APCloudyClient
    :ivar project_id: The project ID for which jobs are managed.
    :type project_id: Int
    """

    def __init__(self, client: 'APCloudyClient', project_id: int):
        self.client = client
        self.project_id = project_id

    def run(self, spider_name: str, units: Optional[int] = None, job_args: Optional[Dict[str, Any]] = None,
            priority: Optional[int] = None, tags: Optional[List[str]] = None) -> Job:
        """
        Run a spider job

        Args:
            spider_name: Name of the spider to run
            units: Number of units (parallel instances) to run
            job_args: Arguments to pass to the spider
            priority: Job priority (higher = more priority)
            tags: Tags for job organization

        Returns:
            Job: The created job instance
        """
        # Validate configuration before using config values
        config.validate()
        data = {
            'job_id': config.current_job_id,
            'spider': spider_name,
            'project': self.project_id,
            'units': units or config.default_units,
            'job_args': job_args or {},
            'priority': priority or config.default_priority,
            'tags': tags or []
        }

        response = self.client.http_request('POST', 'job/run', json=data)
        return Job.from_dict(response['job'])

    def get(self, job_id: str) -> Job:
        """
        Get job details

        Args:
            job_id: Job ID

        Returns:
            Job: Job instance with current status
        """
        try:
            response = self.client.http_request('GET', f'jobs/{job_id}')
            return Job.from_dict(response)
        except APIError as e:
            if e.status_code == 404:
                raise JobNotFoundError(f"Job {job_id} not found")
            raise

    def list(self, state: Optional[JobState] = None, spider: Optional[str] = None,
             count: Optional[int] = None, offset: Optional[int] = None, tags: Optional[List[str]] = None) -> List[Job]:
        """
        List jobs for the project

        Args:
            state: Filter by job state
            spider: Filter by spider name
            count: Number of jobs to return (max 1000)
            offset: Offset for pagination
            tags: Filter by tags

        Returns:
            List[Job]: List of jobs
        """
        # Validate configuration before using config values
        config.validate()

        params = {
            'project': self.project_id,
            'count': min(count or config.default_page_size, config.max_page_size),
            'offset': offset or 0
        }

        if state:
            params['state'] = state.value
        if spider:
            params['spider'] = spider
        if tags:
            params['tags'] = ','.join(tags)

        response = self.client.http_request('GET', 'jobs/list', params=params)
        return [Job.from_dict(job_data) for job_data in response['jobs']]

    def cancel(self, job_id: str) -> bool:
        """
        Cancel a running job

        Args:
            job_id: Job ID to cancel

        Returns:
            bool: True if canceled successfully
        """
        try:
            self.client.http_request('POST', f'jobs/{job_id}/cancel')
            return True
        except APIError as e:
            if e.status_code == 404:
                raise JobNotFoundError(f"Job {job_id} not found")
            return False

    def delete(self, job_id: str) -> bool:
        """
        Delete a job and its data

        Args:
            job_id: Job ID to delete

        Returns:
            bool: True if deleted successfully
        """
        try:
            self.client.http_request('DELETE', f'jobs/{job_id}')
            return True
        except APIError as e:
            if e.status_code == 404:
                raise JobNotFoundError(f"Job {job_id} not found")
            return False

    def get_logs(self, job_id: str, offset: int = 0, count: int = 1000) -> List[str]:
        """
        Get job logs

        Args:
            job_id: Job ID
            offset: Log offset
            count: Number of log lines to return

        Returns:
            List[str]: Log lines
        """
        params = {'offset': offset, 'count': count}
        response = self.client.http_request('GET', f'jobs/{job_id}/logs', params=params)
        return response.get('logs', [])

    def get_items(self, job_id: str, offset: int = 0, count: int = 1000) -> List[Dict[str, Any]]:
        """
        Get scraped items from a job

        Args:
            job_id: Job ID
            offset: Item offset
            count: Number of items to return

        Returns:
            List[Dict]: Scraped items
        """
        params = {'offset': offset, 'count': count}
        response = self.client.http_request('GET', f'jobs/{job_id}/items', params=params)
        return response.get('items', [])

    def iter_items(self, job_id: str, batch_size: int = 1000) -> Iterator[Dict[str, Any]]:
        """
        Iterate over all items from a job

        Args:
            job_id: Job ID
            batch_size: Items per batch

        Yields:
            Dict: Individual scraped items
        """
        offset = 0
        while True:
            items = self.get_items(job_id, offset=offset, count=batch_size)
            if not items:
                break

            for item in items:
                yield item

            offset += len(items)
            if len(items) < batch_size:
                break

    def wait_for_completion(self, job_id: str, poll_interval: Optional[int] = None,
                            timeout: Optional[int] = None) -> Job:
        """
        Wait for job completion

        Args:
            job_id: Job ID to wait for
            poll_interval: Seconds between status checks (uses config default if not provided)
            timeout: Max seconds to wait (uses config default if not provided)

        Returns:
            Job: Final job state
        """
        # Validate configuration before using config values
        config.validate()

        poll_interval = poll_interval or config.default_poll_interval
        timeout = timeout or config.default_job_timeout
        start_time = time.time()

        while True:
            job = self.get(job_id)

            if job.is_finished:
                return job

            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")

            time.sleep(poll_interval)


class SpidersManager:
    """
    Manages spider operations within a specific project.

    This class provides the functionality to list, retrieve, upload, and delete
    spiders associated with a project. It serves as an interface for working
    with spiders in the context of an APCloudyClient instance.

    :ivar client: The client used to interact with the spider API.
    :type client: APCloudyClient
    :ivar project_id: The ID of the project the spiders are associated with.
    :type project_id: int
    """

    def __init__(self, client: 'APCloudyClient', project_id: int):
        self.client = client
        self.project_id = project_id

    def list(self) -> List[Spider]:
        """
        List all spiders in the project

        Returns:
            List[Spider]: Available spiders
        """
        params = {'project': self.project_id}
        response = self.client.http_request('GET', 'spiders/list', params=params)
        return [Spider.from_dict(spider_data) for spider_data in response['spiders']]

    def get(self, spider_name: str) -> Spider:
        """
        Get spider details

        Args:
            spider_name: Name of the spider

        Returns:
            Spider: Spider details
        """
        try:
            params = {'project': self.project_id}
            response = self.client.http_request('GET', f'spiders/{spider_name}', params=params)
            return Spider.from_dict(response)
        except APIError as e:
            if e.status_code == 404:
                raise SpiderNotFoundError(f"Spider {spider_name} not found")
            raise

    def upload(self, spider_file: str, spider_name: Optional[str] = None) -> bool:
        """
        Upload a spider file

        Args:
            spider_file: Path to spider file
            spider_name: Override spider name (optional)

        Returns:
            bool: True if uploaded successfully
        """
        with open(spider_file, 'rb') as f:
            return self.upload_from_file(f, spider_name or spider_file)

    def upload_from_file(self, file_obj: BinaryIO, spider_name: str) -> bool:
        """
        Upload spider from file object

        Args:
            file_obj: File-like object containing spider code
            spider_name: Name for the spider

        Returns:
            bool: True if uploaded successfully
        """
        files = {'spider_file': (spider_name, file_obj, 'text/plain')}
        data = {'project': self.project_id, 'spider_name': spider_name}

        response = self.client.http_request('POST', 'spiders/upload', data=data, files=files)
        return response.get('success', False)

    def delete(self, spider_name: str) -> bool:
        """
        Delete a spider

        Args:
            spider_name: Name of spider to delete

        Returns:
            bool: True if deleted successfully
        """
        try:
            data = {'project': self.project_id}
            self.client.http_request('DELETE', f'spiders/{spider_name}', json=data)
            return True
        except APIError as e:
            if e.status_code == 404:
                raise SpiderNotFoundError(f"Spider {spider_name} not found")
            return False


class ProjectManager:
    """Manages a specific project"""

    def __init__(self, client: 'APCloudyClient', project_id: int):
        self.client = client
        self.project_id = project_id
        self.jobs = JobsManager(client, project_id)
        self.spiders = SpidersManager(client, project_id)

    def get_info(self) -> Project:
        """
        Get project information

        Returns:
            Project: Project details
        """
        try:
            response = self.client.http_request('GET', f'project/{self.project_id}')
            return Project.from_dict(response)
        except APIError as e:
            if e.status_code == 404:
                raise ProjectNotFoundError(f"Project {self.project_id} not found")
            raise


class APCloudyClient:
    """
    Represents a client for interacting with the APCloudy API.

    This class provides methods to make authenticated HTTP requests, manage projects
    (e.g., retrieval, creation, and listing), and validate the connection with the APCloudy API.
    The client supports additional features such as retry logic for transient errors
    and rate-limiting compliance.

    :ivar api_key: The API key is used for authentication with the APCloudy API.
    :type api_key: Str
    :ivar base_url: The base URL for the APCloudy API.
    :type base_url: Str
    :ivar session: The session object used to handle HTTP requests.
    :type session: Requests.Session
    """

    def __init__(self, api_key: str = ''):
        """
        Initialize APCloudy client

        Args:
            api_key: Your APCloudy API key
        """
        # Set API key and validate configuration
        if api_key:
            config.api_key = api_key

        config.validate()

        self.api_key = config.api_key
        self.base_url = config.base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': f'apcloudy-client/0.1.0'
        })

        # Set request timeout from config
        self.session.timeout = config.request_timeout

    def http_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make API request with retry logic

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            Dict: API response data
        """
        url = urljoin(f"{self.base_url}/", endpoint)

        for attempt in range(config.max_retries + 1):
            try:
                response = self.session.request(method, url, **kwargs)

                # Handle rate limiting with retry
                if response.status_code == 429:
                    retry_after = config.rate_limit_delay
                    if attempt < config.max_rate_limit_retries:
                        time.sleep(retry_after)
                        continue
                    raise RateLimitError(
                        f"Rate limit exceeded. Retry after {retry_after} seconds",
                        status_code=429,
                        response_data={'retry_after': retry_after}
                    )

                # Handle authentication errors
                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key", status_code=401)

                if response.status_code == 409:
                    raise APIError(response.json().get('error'), status_code=409)

                # Handle other client/server errors
                if not response.ok:
                    try:
                        error_data = response.json()
                        message = error_data.get('message', f'HTTP {response.status_code}')
                    except (ValueError, json.JSONDecodeError):
                        message = f'HTTP {response.status_code}: {response.text}'

                    # Retry on server errors (5xx) but not client errors (4xx)
                    if response.status_code >= 500 and attempt < config.max_retries:
                        delay = config.retry_delay * (config.backoff_factor ** attempt)
                        time.sleep(delay)
                        continue

                    raise APIError(message, status_code=response.status_code)

                # Return JSON response on success
                return response.json()

            except requests.RequestException as e:
                if attempt < config.max_retries:
                    delay = config.retry_delay * (config.backoff_factor ** attempt)
                    time.sleep(delay)
                    continue
                raise APIError(f"Request failed: {str(e)}")

        # This should never be reached, but just in case
        raise APIError("Maximum retries exceeded")

    def get_project(self, project_id: int) -> ProjectManager:
        """
        Get the project manager

        Args:
            project_id: Project ID

        Returns:
            ProjectManager: Project manager instance
        """
        return ProjectManager(self, project_id)

    def list_projects(self) -> List[Project]:
        """
        List all accessible projects

        Returns:
            List[Project]: Available projects
        """
        response = self.http_request('GET', 'projects/list')
        return [Project.from_dict(proj_data) for proj_data in response['projects']]

    def create_project(self, name: str, description: str = "") -> Project:
        """
        Create a new project

        Args:
            name: Project name
            description: Project description

        Returns:
            Project: Created project
        """
        data = {'name': name, 'description': description}
        response = self.http_request('POST', 'projects/create', json=data)
        return Project.from_dict(response)

    def verify(self) -> bool:
        """
        Test API connection and authentication

        Returns:
            bool: True if connection successful
        """
        try:
            self.http_request('GET', 'verify')
            return True
        except Exception:
            return False
