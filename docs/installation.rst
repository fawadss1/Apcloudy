Installation
============

System Requirements
-------------------

APCloudy requires Python 3.7 or higher. It has been tested on:

* Python 3.7+
* Python 3.8+
* Python 3.9+
* Python 3.10+
* Python 3.11+
* Python 3.12+

Operating Systems
-----------------

APCloudy is compatible with:

* Windows
* macOS
* Linux

Installing APCloudy
-------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~

Install APCloudy using pip:

.. code-block:: bash

   pip install apcloudy

From Source
~~~~~~~~~~~

To install from source, clone the repository and install:

.. code-block:: bash

   git clone https://github.com/yourusername/apcloudy.git
   cd apcloudy
   pip install -e .

Dependencies
------------

APCloudy automatically installs the following dependencies:

* **requests**: For HTTP API communication
* **tabulate**: For formatting output tables

Verifying Installation
----------------------

To verify that APCloudy is installed correctly, run:

.. code-block:: python

   import apcloudy
   print(apcloudy.__version__)

Or test the basic functionality:

.. code-block:: python

   from apcloudy import APCloudyClient

   # This will validate the import works
   client = APCloudyClient()
   print("APCloudy installed successfully!")

Development Installation
------------------------

If you plan to contribute to APCloudy, install the development dependencies:

.. code-block:: bash

   git clone https://github.com/yourusername/apcloudy.git
   cd apcloudy
   pip install -e ".[dev]"

This will install additional packages needed for testing and development.

Upgrading
---------

To upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade apcloudy

Uninstalling
------------

To uninstall APCloudy:

.. code-block:: bash

   pip uninstall apcloudy
