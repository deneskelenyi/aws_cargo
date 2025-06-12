What it is

It's just a small python script I run every hour to check packages at awscargo.com. 
The service only supports a single notification email per account, and doesn't seem to send repeat notifications when many packages came in at the same time. 

I normally dump my on-line orders into my "Notes" app on my iPhone, and I end up with a colon delimited list of description:tracking number pairs. 

The front (front.py) is just a minimal Gradio app, where I paste the notes from my phone. It splits them up, trims them from spaces and puts them into a database. 

The main app runs every hour between work hours (8am - 5pm) from crontab. It performs a log-in to awscargo.com, goes to the "My packages" page and extracts the table from there, using Beautiful Soup. It then checks each row for a tracking number and the price of tax/shipment. 

After that, it searches the database for orders (inserted from the Gradio app), and tries to match them up with completed shipments. 

If everything goes OK, you end up with a list of packages, containing the import/shipment price and a name. If there is no order found, then it's just a tracking number and a price. 

It then sends them via Pushover. 


Requirements: 

You will need a working installation of Chrome. A matching version of selenium chrome-driver, and everything else in requirements.txt. 

Using a virtual environment is recommended. 

The app uses the awscargo.com login credentials from.env file (and everything else where an os.getenv is used).

It's very niche and very local to a Costa Rican service, but who knows, maybe it helps someone. 


