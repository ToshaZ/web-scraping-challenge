#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # HTML Object
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')


    # NASA Mars News
    # Retrieve the first article title and teaser
    news_title = soup.find_all('div', class_ = 'content_title')[1].text
    news_p = soup.find('div', class_='article_teaser_body').text


    # JPL Mars Space Images - Featured Image
    # URL of page to be scraped
    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    main_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    browser.visit(image_url)

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    image_soup = bs(html_image, "html.parser")

    image_path = image_soup.find('img', class_='headerimage fade-in')['src']

    #print(image_path)
    featured_image_url = main_url + image_path


    # Mars Facts
    # URL of page to be scraped
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    # HTML Object
    #facts_html = browser.html

    # Use Pandas to scrape the table
    facts_table = pd.read_html(facts_url)

    #facts_table
    # Create dataframe from the correct table
    mars_df = facts_table[0]

    # Rename columns
    mars_df.columns = ['Description','Mars']

    # Set Index to be description
    mars_df = mars_df.set_index('Description')

    # Use Pandas to convert the data to a HTML table string
    mars_facts = mars_df.to_html()


    # Mars Hemispheres
    # URL of page to be scraped
    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_url)
    main_mars_url = 'https://astrogeology.usgs.gov/'

    # HTML Object
    mars_html = browser.html

    # Parse HTML with Beautiful Soup
    mars_soup = bs(mars_html, "html.parser")

    # Create dictionary to store titles & URLs
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    mars_path = mars_soup.find_all('div', class_='description')

    # Loop through for each image and URL
    for i in mars_path:
        
        # Save title
        title = i.find('h3').text
        
        # Collect image
        image_url = i.find('a', class_='itemLink product-item')['href']
        img_page = main_mars_url + image_url
        browser.visit(img_page)
        page_html = browser.html
        page_soup = bs(page_html, "html.parser")
        img_url = page_soup.find('img', class_='wide-image')['src']
        full_page = main_mars_url + img_url
        
        #print(img_page)
        #print(full_page)
        
        # Create dictionary
        hem_dict = {
            'title': title,
            'img_url': full_page
        }

        # Append dictionary
        hemisphere_image_urls.append(hem_dict)
        

    mars = {
        "news_title": news_title,
        "latest_news": news_p,
        "featured_img": featured_image_url,
        "mars_facts": mars_facts,
        "hemisphere_img": hemisphere_image_urls
    }


    browser.quit()

    return mars