"""
Example usage demonstrating the updated APCloudy client with configuration:
"""

import logging
import requests
import xml.etree.ElementTree as ET
from apcloudy import APCloudyClient, config
from apcloudy.models import JobState
from apcloudy.utils import chunk_urls


def get_sitemap_urls():
    sitemap_url = 'https://uk.rs-online.com/uk-sitemap.xml'
    resp = requests.get(sitemap_url)
    if not resp.ok:
        raise Exception(f"Failed to fetch sitemap: {resp.status_code}")

    root = ET.fromstring(resp.content)
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [
        loc.text for loc in root.findall('.//ns:loc', ns)
        if 'uk_products_' in loc.text
    ]

    if not urls:
        raise Exception("No product URLs found in the sitemap.")

    logging.info(f"Got {len(urls)} sitemap urls.")
    return urls


client = APCloudyClient("sk_1s_PQ8FhpxCumRV4g9ilfXaLdyE1WzjH5nTtR1mgNl4")

# if client.verify():
#     print("✅ Connected to APCloudy successfully!")
# else:
#     print("❌ Failed to connect to APCloudy")

project = client.get_project(10001)
sp = client.create_project('kkkfdsf')
# print(sp)

# for i in range(2):
#     project.jobs.run('Rs_Spider',
#                      job_args={'sitemap_urls': f'https://example.com{i}'})

exit()

# Run spiders with config-driven defaults
for url_chunk in chunk_urls(get_sitemap_urls(), 5):
    url_chunk_str = ','.join(url_chunk)
    logging.info(f"Starting Rs_Spider with URL len: {len(url_chunk)}")

    # Now uses config defaults: units=2, priority=0
    job = project.jobs.run(
        'Rs_Spider',
        # units parameter is optional - uses config.default_units (2) if not provided
        job_args={
            'sitemap_urls': url_chunk_str
        }
    )

    print(f"Started job {job.job_id} with {job.units} units")

    # Wait for completion with config defaults
    # poll_interval and timeout now use config.default_poll_interval and config.default_job_timeout
    try:
        completed_job = project.jobs.wait_for_completion(job.job_id)
        print(f"Job {completed_job.job_id} completed with state: {completed_job.state}")

        # Get items with automatic retry logic
        items = list(project.jobs.iter_items(job.job_id))
        print(f"Scraped {len(items)} items")

    except TimeoutError as e:
        print(f"Job timed out: {e}")
    except Exception as e:
        print(f"Job failed: {e}")

print(f"All jobs completed. Configuration used:")
print(f"- Base URL: {config.base_url}")
print(f"- Default units: {config.default_units}")
print(f"- Request timeout: {config.request_timeout}s")
print(f"- Max retries: {config.max_retries}")
print(f"- Default page size: {config.default_page_size}")
