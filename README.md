# Mission to Mars:
## Webscraping with Splinter (Browser and ChromeDriver), MongoDB and Flask

### Overview

Using Browser and Chrome Driver from Splinter, 3 different websites can be scraped for articles, images and a datatable - all pertaining to the planet Mars.  The scraped data is stored in MongoDB.  The Flask app is connected to the mars_app database in Mongo and renders the data as coded by the index.html template.  Clicking the 'Scrape New Data' will retrieve the latest article and featured image from NASA's website.

### `scraping.py`

This file contains the python functions which code the scraping for the 4 main sections rendered in the Flask app.

### `index.html`

This is the .html template which is rendered by the Flask app.
Using bootstrap elements, the hemisphere images were made responsive, and the colors of the jumbotron header and the scraping buttons were changed.

### `app.py`

This file contains the python code which initiates the Flask app, calls the scraping functions and connects to the Mongo database to retrieve the scraped data.

When this file is run, the rendered output looks similar to this, however 3 of the hemispheres have been truncated from this image for readability here:

![rendered](https://github.com/lnshewmo/Mission-to-Mars/blob/main/index_rendered.png)

### `Mission_to_Mars_Challenge.ipynb`

This is the jupyter notebook file from which the scraping.py file was exported.


