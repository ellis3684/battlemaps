# battlemaps

Battle Maps is a web app written primarily in Python's Django framework, 
that uses a Google Maps like interface and allows you to search for historical battles that took place near you. 

This database contains coordinate data for over 4,000 battles - all of which were scraped from Wikipedia using BeautifulSoup. 
The map interface was developed using Google Maps' Javascript API. Finally, the app itself is hosted on a Linux server on a DigitalOcean droplet and can be accessed at https://battlemaps.app/ - where the battle data is stored in a Postgres database.

I've separated this project into two main directories: one ('scrape_battles') which shows the code written in Python's BeautifulSoup library which extracted
all of the battle data used in this project from Wikipedia. The second main directory ('battlesnearme') contains the Django project folder for this app.

As a history nerd, I had a lot of fun creating this project, and I'm very excited to be able to share this with others. Enjoy!
