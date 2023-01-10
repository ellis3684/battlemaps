# battlemaps

Battle Maps is a web app written primarily in Python's Django framework, 
that uses a Google Maps like interface and allows you to search for historical battles that took place near you. 

This database contains coordinate data for over 4,000 battles - all of which were scraped from Wikipedia using BeautifulSoup. 
The map interface was developed using Google Maps' Javascript API. ~~Finally, the app itself is deployed to Heroku and
can be accessed at https://battlesnearme.herokuapp.com/ - where the battle data is stored in a Postgres database.~~ As of December 2022, Battle Maps
is no longer hosted on Heroku due to Heroku shutting down free dynos. In the future, Battle Maps will be migrating to a Digitalocean droplet.

I've separated this project into two main directories: one ('scrape_battles') which shows the code written in Python's BeautifulSoup library which extracted
all of the battle data used in this project from Wikipedia. The second main directory ('battlesnearme') contains the Django project folder for this app.

As a history nerd, I had a lot of fun creating this project (check out my [project diary](https://docs.google.com/document/d/12CHt1vLfyASo1WSwXVvI1_IysZv9BSkMueWTbdzbBMY/edit?usp=sharing) if you'd like to see my thought process) - and I'm very excited to be able to share this with others. Enjoy!
