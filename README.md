# Construction-Cam-WS


### Overview

This web scraper was created to help gather links to construction cameras from the Denver Skyscraperpage forums. These links can be hard to track down because the forum is over 450 pages long and offers no search functionality whatsoever. Most of the sites that offer construction camera services require a sign in unless you have the correct hidden url. These links can be used to view live construction feeds from various development companies and timelapses of different construction projects in the Denver metro area. 


### How to use

- Fork and/or clone down this repo and cd into the root directory. 
- To run the scraper, simply use `python3 scraper.py`
- You must have Python3, Selenium, BeautifulSoup, tdqm, and Pandas installed to run this application. 
- Once the scrape is complete and JSON file will be generated within `results/`. The file name will simply be a timestamp from when the script is finished running. The data will be formatted as a JSON object that includes two keys: `page` - An integer that represents the page number of the forum that the link was found on and `links` - A list of the links found on that page. 

Note: This scraper takes a very long time to run due to the amount of comments that need to be parsed. 

