"""
Configuration settings for the APCloudy client.

This module provides a `Config` class that encapsulates all the configuration
settings required for interacting with the APCloudy client. These settings
include API-related configurations, job-specific defaults, HTTP connection
options, pagination limits, file upload constraints, and logging preferences.
"""


class Config:
    """Configuration class for APCloudy client settings"""

    def __init__(self, settings=None):
        self.base_url = self._build_base_url(settings)
        self.api_key = None
        self.project_id = None
        self.current_job_id = None

        # Job settings
        self.default_units = 2
        self.default_priority = 0

        # HTTP settings
        self.request_timeout = 30
        self.max_retries = 3
        self.retry_delay = 1
        self.backoff_factor = 2

        # Logging
        self.log_level = "INFO"
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @staticmethod
    def _build_base_url(settings):
        """Build base URL from settings with /api/client suffix"""
        if not settings:
            return None

        base_url = settings.get('APCLOUDY_URL')
        return f"{base_url.rstrip('/')}/api/client" if base_url else None

    def update_from_settings(self, settings):
        """Update configuration from Scrapy settings"""
        if settings:
            new_base_url = self._build_base_url(settings)
            if new_base_url:
                self.base_url = new_base_url

    def validate(self) -> bool:
        """Validate configuration settings"""
        if not self.base_url:
            raise ValueError("APCLOUDY_URL is required. Please set it in your Scrapy settings.")

        if not self.api_key:
            raise ValueError("API key is required. Please pass it to the client.")

        if self.default_units < 1:
            raise ValueError("Default units must be at least 1")

        if self.request_timeout <= 0:
            raise ValueError("Request timeout must be positive")

        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")

        return True


# Global configuration instance
config = Config()
