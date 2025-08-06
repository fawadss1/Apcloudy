Quick Start Guide
=================

This guide will help you get started with APCloudy in just a few minutes.

Prerequisites
-------------

Before you begin, make sure you have:

1. Python 3.7 or higher installed
2. An APCloudy account and API key
3. APCloudy package installed (see :doc:`installation`)

Getting Your API Key
--------------------

1. Log in to your APCloudy dashboard
2. Navigate to Account Settings > API Keys
3. Generate a new API key or copy an existing one
4. Keep this key secure - you'll need it for authentication

Basic Usage
-----------

Initialize the Client
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from apcloudy import APCloudyClient

   # Initialize with your API key
   client = APCloudyClient("your-api-key-here")

   # Alternatively, set via environment variable
   import os
   os.environ['APCLOUDY_API_KEY'] = 'your-api-key-here'
   client = APCloudyClient()

Working with Projects
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # List all projects
   projects = client.get_projects()
   print(f"Found {len(projects)} projects")

   # Get a specific project
   project = client.get_project("project-id")
   print(f"Project: {project.name}")

   # Create a new project
   new_project = client.create_project(
       name="My New Project",
       description="A sample web scraping project"
   )

Managing Spiders
~~~~~~~~~~~~~~~~

.. code-block:: python

   # List spiders in a project
   spiders = client.get_spiders("project-id")

   # Get spider details
   spider = client.get_spider("project-id", "spider-name")
   print(f"Spider: {spider.name}")

   # Deploy a spider (upload spider code)
   client.deploy_spider("project-id", "spider-name", spider_code)

Running Jobs
~~~~~~~~~~~~

.. code-block:: python

   # Start a scraping job
   job = client.start_job("project-id", "spider-name")
   print(f"Job started with ID: {job.id}")

   # Check job status
   job_status = client.get_job(job.id)
   print(f"Job state: {job_status.state}")

   # List all jobs for a project
   jobs = client.get_jobs("project-id")

   # Stop a running job
   client.stop_job(job.id)

Complete Example
----------------

Here's a complete example that demonstrates the main features:

.. code-block:: python

   from apcloudy import APCloudyClient
   import time

   # Initialize client
   client = APCloudyClient("your-api-key-here")

   try:
       # List projects
       projects = client.get_projects()
       if projects:
           project = projects[0]
           print(f"Using project: {project.name}")

           # List spiders
           spiders = client.get_spiders(project.id)
           if spiders:
               spider = spiders[0]
               print(f"Found spider: {spider.name}")

               # Start a job
               job = client.start_job(project.id, spider.name)
               print(f"Started job: {job.id}")

               # Monitor job progress
               while True:
                   job_status = client.get_job(job.id)
                   print(f"Job state: {job_status.state}")

                   if job_status.state in ['completed', 'failed']:
                       break

                   time.sleep(5)  # Wait 5 seconds before checking again

               print("Job finished!")
           else:
               print("No spiders found in project")
       else:
           print("No projects found")

   except Exception as e:
       print(f"Error: {e}")

Environment Variables
--------------------

You can configure APCloudy using environment variables:

.. code-block:: bash

   # Set your API key
   export APCLOUDY_API_KEY="your-api-key-here"

   # Set custom API endpoint (optional)
   export APCLOUDY_BASE_URL="https://api.apcloudy.com"

.. code-block:: python

   # Client will automatically use environment variables
   client = APCloudyClient()

Error Handling
--------------

APCloudy provides specific exceptions for different error conditions:

.. code-block:: python

   from apcloudy import APCloudyClient
   from apcloudy.exceptions import (
       APIError,
       AuthenticationError,
       ProjectNotFoundError,
       RateLimitError
   )

   client = APCloudyClient("your-api-key")

   try:
       projects = client.get_projects()
   except AuthenticationError:
       print("Invalid API key")
   except RateLimitError:
       print("Rate limit exceeded, please wait")
   except ProjectNotFoundError:
       print("Project not found")
   except APIError as e:
       print(f"API error: {e}")

Next Steps
----------

Now that you've got the basics down, explore these topics:

* :doc:`user_guide` - Detailed usage instructions
* :doc:`api_reference` - Complete API documentation
* :doc:`examples` - More code examples
* :doc:`configuration` - Advanced configuration options
