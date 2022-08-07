#!/usr/bin/env python
# coding: utf-8

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object
html = browser.html
news_soup = soup(html, 'html.parser')

# parent element
slide_elem = news_soup.select_one('div.list_text')
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts
df = pd.read_html('https://galaxyfacts-mars.com')[0]

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

browser.is_element_present_by_css("div.result-list", wait_time=1)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

hemi_links = browser.find_by_css("a.product-item img")

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(len(hemi_links)):
    
    hemi_data= {}
    
    browser.find_by_css("a.product-item img")[i].click()
    inspect_element = browser.links.find_by_text("Sample").first
    hemi_data['hemi_url'] = inspect_element["href"]
    hemi_data['hemi_title'] = browser.find_by_css('h2.title').text

    hemisphere_image_urls.append(hemi_data)
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
