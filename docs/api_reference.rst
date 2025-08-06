API Reference
=============

This section provides detailed documentation for all APCloudy classes, methods, and functions.

.. currentmodule:: apcloudy

Client
------

.. autoclass:: APCloudyClient
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

Job State
~~~~~~~~~

.. autoclass:: apcloudy.models.JobState
   :members:
   :undoc-members:
   :show-inheritance:

Job
~~~

.. autoclass:: apcloudy.models.Job
   :members:
   :undoc-members:
   :show-inheritance:

Spider
~~~~~~

.. autoclass:: apcloudy.models.Spider
   :members:
   :undoc-members:
   :show-inheritance:

Project
~~~~~~~

.. autoclass:: apcloudy.models.Project
   :members:
   :undoc-members:
   :show-inheritance:

Managers
--------

Project Manager
~~~~~~~~~~~~~~~

.. automodule:: apcloudy.project_manager
   :members:
   :undoc-members:
   :show-inheritance:

Jobs Manager
~~~~~~~~~~~~

.. automodule:: apcloudy.jobs_manager
   :members:
   :undoc-members:
   :show-inheritance:

Spiders Manager
~~~~~~~~~~~~~~~

.. automodule:: apcloudy.spiders_manager
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
-------------

.. automodule:: apcloudy.config
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
----------

.. automodule:: apcloudy.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Base Exception
~~~~~~~~~~~~~~

.. autoexception:: apcloudy.exceptions.APCloudyException
   :members:
   :show-inheritance:

API Error
~~~~~~~~~

.. autoexception:: apcloudy.exceptions.APIError
   :members:
   :show-inheritance:

Authentication Error
~~~~~~~~~~~~~~~~~~~~

.. autoexception:: apcloudy.exceptions.AuthenticationError
   :members:
   :show-inheritance:

Project Not Found Error
~~~~~~~~~~~~~~~~~~~~~~~

.. autoexception:: apcloudy.exceptions.ProjectNotFoundError
   :members:
   :show-inheritance:

Rate Limit Error
~~~~~~~~~~~~~~~~

.. autoexception:: apcloudy.exceptions.RateLimitError
   :members:
   :show-inheritance:

Utilities
---------

.. automodule:: apcloudy.utils
   :members:
   :undoc-members:
   :show-inheritance:

Method Reference
----------------

APCloudyClient Methods
~~~~~~~~~~~~~~~~~~~~~~

Authentication
^^^^^^^^^^^^^^

.. automethod:: APCloudyClient.__init__

Project Operations
^^^^^^^^^^^^^^^^^^

.. automethod:: APCloudyClient.get_projects
.. automethod:: APCloudyClient.get_project
.. automethod:: APCloudyClient.create_project
.. automethod:: APCloudyClient.update_project
.. automethod:: APCloudyClient.delete_project

Spider Operations
^^^^^^^^^^^^^^^^^

.. automethod:: APCloudyClient.get_spiders
.. automethod:: APCloudyClient.get_spider
.. automethod:: APCloudyClient.deploy_spider
.. automethod:: APCloudyClient.update_spider
.. automethod:: APCloudyClient.delete_spider

Job Operations
^^^^^^^^^^^^^^

.. automethod:: APCloudyClient.get_jobs
.. automethod:: APCloudyClient.get_job
.. automethod:: APCloudyClient.start_job
.. automethod:: APCloudyClient.stop_job
.. automethod:: APCloudyClient.delete_job

Data Operations
^^^^^^^^^^^^^^^

.. automethod:: APCloudyClient.get_job_data
.. automethod:: APCloudyClient.stream_job_data
.. automethod:: APCloudyClient.get_job_logs

Type Definitions
----------------

The following types are used throughout the APCloudy API:

.. code-block:: python

   from typing import Dict, List, Optional, Any, Union
   from datetime import datetime

   # Common type aliases
   ProjectID = str
   SpiderName = str
   JobID = str
   APIKey = str

   # Data structures
   JobSettings = Dict[str, Any]
   SpiderSettings = Dict[str, Any]
   ProjectMetadata = Dict[str, Any]

   # Response types
   JobData = List[Dict[str, Any]]
   LogEntry = Dict[str, Union[str, datetime]]

Constants
---------

Job States
~~~~~~~~~~

.. code-block:: python

   class JobState:
       SCHEDULED = "scheduled"
       RUNNING = "running"
       COMPLETED = "completed"
       DELETED = "deleted"

Default Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   DEFAULT_BASE_URL = "https://api.apcloudy.com"
   DEFAULT_TIMEOUT = 30
   DEFAULT_RETRIES = 3
   DEFAULT_RATE_LIMIT = 100  # requests per minute

HTTP Status Codes
~~~~~~~~~~~~~~~~~

.. code-block:: python

   HTTP_OK = 200
   HTTP_CREATED = 201
   HTTP_BAD_REQUEST = 400
   HTTP_UNAUTHORIZED = 401
   HTTP_FORBIDDEN = 403
   HTTP_NOT_FOUND = 404
   HTTP_RATE_LIMITED = 429
   HTTP_SERVER_ERROR = 500
