"""Data models for APCloudy"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from tabulate import tabulate

from .config import config


class JobState(Enum):
    """Job execution states"""
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    DELETED = "deleted"


@dataclass
class Job:
    """Represents a scraping job"""
    job_id: str
    spider_name: str
    state: JobState
    project_id: str = ""
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    items_scraped: int = 0
    requests_made: int = 0
    job_args: Dict[str, Any] = field(default_factory=dict)
    units: int = 1
    logs_url: Optional[str] = None
    items_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Job':
        """Create Job instance from API response"""
        config.current_job_id = data['job_id']

        # Create the Job instance
        job = cls(
            job_id=data['job_id'],
            spider_name=data['spider_name'],
            state=JobState(data['status']),
            project_id=data.get('project_id', ''),
            created_at=cls._parse_datetime(data.get('created_at')),
            started_at=cls._parse_datetime(data.get('started_at')),
            finished_at=cls._parse_datetime(data.get('finished_at')),
            items_scraped=data.get('items_scraped', 0),
            requests_made=data.get('requests_made', 0),
            job_args=data.get('job_args', {}),
            units=data.get('units', 1),
            logs_url=data.get('logs_url'),
            items_url=data.get('items_url'),
        )

        # Display job data in table format with columns
        headers = ["Job ID", "Spider Name", "State", "Project ID", "Created At", "Started At", "Finished At", "Items", "Requests", "Units", "Duration"]
        row_data = [
            job.job_id,
            job.spider_name,
            job.state.value,
            job.project_id or "N/A",
            job.created_at.strftime("%Y-%m-%d %H:%M:%S") if job.created_at else "N/A",
            job.started_at.strftime("%Y-%m-%d %H:%M:%S") if job.started_at else "N/A",
            job.finished_at.strftime("%Y-%m-%d %H:%M:%S") if job.finished_at else "N/A",
            job.items_scraped,
            job.requests_made,
            job.units,
            f"{job.duration:.2f}s" if job.duration else "N/A"
        ]

        print("\n" + "="*120)
        print("JOB DETAILS")
        print("="*120)
        print(tabulate([row_data], headers=headers, tablefmt="grid"))
        print("="*120 + "\n")

        return job

    @staticmethod
    def _parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string from API"""
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None

    @property
    def is_finished(self) -> bool:
        """Check if job is finished (success or failed)"""
        return self.state in (JobState.COMPLETED, JobState.DELETED)

    @property
    def duration(self) -> Optional[float]:
        """Get job duration in seconds"""
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None


@dataclass
class Spider:
    """Represents a spider"""
    name: str
    version: str = "1.0.0"
    description: str = ""
    project_id: str = ""
    settings: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Spider':
        """Create Spider instance from API response"""
        spider = cls(
            name=data['name'],
            version=data.get('version', '1.0.0'),
            description=data.get('description', ''),
            project_id=data.get('project_id', ''),
            settings=data.get('settings', {}),
            tags=data.get('tags', [])
        )

        # Display spider data in table format with columns
        headers = ["Name", "Version", "Description", "Project ID", "Tags", "Settings Count"]
        row_data = [
            spider.name,
            spider.version,
            spider.description or "N/A",
            spider.project_id or "N/A",
            ", ".join(spider.tags) if spider.tags else "N/A",
            len(spider.settings)
        ]

        print("SPIDER DETAILS")
        print(tabulate([row_data], headers=headers, tablefmt="grid"))
        return spider


@dataclass
class Project:
    """Represents a project"""
    project_id: str
    org_name: str
    name: str
    description: str = ""
    created_at: Optional[datetime] = None
    spider_count: int = 0
    job_count: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create Project instance from API response"""
        project = cls(
            project_id=data['project_id'],
            org_name=data['organization_name'],
            name=data['name'],
            description=data.get('description', ''),
            created_at=Job._parse_datetime(data.get('created_at')),
            spider_count=data.get('spider_count', 0),
            job_count=data.get('job_count', 0)
        )

        headers = ["ID", "Org Name", "Name", "Description", "Created At", "Spider Count", "Job Count"]
        row_data = [
            project.project_id,
            project.org_name,
            project.name,
            project.description or "N/A",
            project.created_at.strftime("%Y-%m-%d %H:%M:%S") if project.created_at else "N/A",
            project.spider_count,
            project.job_count
        ]

        print("PROJECT DETAILS")
        print(tabulate([row_data], headers=headers, tablefmt="grid"))
        return project
