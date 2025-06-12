# AWS Cargo Package Tracker
==========================

**Overview**
------------

This is a Python script that tracks packages at Awscargo.com using Beautiful Soup and Selenium ChromeDriver.

**What it does**

The script runs every hour between 8am-5pm to check for new packages on Awscargo.com. It extracts the tracking numbers and prices from 
the "My Packages" page, then searches for matching orders in a database. If an order is found, it matches up with the package 
information. The results are sent via Pushover.

**Requirements**

*   A working installation of Chrome
*   Matching version of Selenium ChromeDriver
*   Requirements listed in `requirements.txt`
*   Virtual environment recommended

**Setup**
---------

1.  Install dependencies using pip: `pip install -r requirements.txt`
2.  Set up a virtual environment (recommended)
3.  Configure the `.env` file with Awscargo.com login credentials

**Frontend**
------------

The frontend is built using Gradio and runs on `front.py`. It takes input from the user's iPhone Notes app, processes it, and stores 
it in a database.

**Backend**
------------

The backend script runs every hour between 8am-5pm from crontab. It performs the following tasks:

1.  Logs into Awscargo.com using Beautiful Soup
2.  Extracts the table from the "My Packages" page
3.  Checks each row for a tracking number and price
4.  Searches the database for matching orders
5.  Sends the results via Pushover

**Usage**
--------

1.  Run `python main.py` to start the script
2.  The script will run every hour between 8am-5pm
3.  Results are sent via Pushover
