
# Import Splinter, BeautifulSoup, and Pandas
import inspect
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape_all():
    # initiate headless driver for deployment, setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # set headless to False to watch the scrape in chrome

    news_title, news_paragraph = mars_news(browser)
    hemispheres = mars_hemispheres(browser)

    # run all scraping functions and store the results in a dict
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres
    }

    browser.quit()
    return data

# Mars News
def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # error handling
    try:
        # parent element
        slide_elem = news_soup.select_one('div.list_text')
        
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # convert df to html format, add bootstrap
    return df.to_html(classes='table table-striped')

def mars_hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.result-list', wait_time=1)

    hemisphere_image_urls = []

    hemi_links = browser.find_by_css('a.product-item img')

    for i in range(len(hemi_links)):

        hemi_data = {}

        browser.find_by_css('a.product-item img')[i].click()
        inspect_element = browser.links.find_by_text('Sample').first
        hemi_data['hemi_url'] = inspect_element['href']
        hemi_data['hemi_title'] = browser.find_by_css('h2.title').text

        hemisphere_image_urls.append(hemi_data)
        browser.back()

    return hemisphere_image_urls

if __name__ == '__main__':
    # if running as a script, print scraped data
    print(scrape_all())