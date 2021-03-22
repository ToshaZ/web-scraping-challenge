#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[6]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# HTML Object
html = browser.html

# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(html, 'html.parser')


# NASA Mars News

# In[7]:


# Retrieve the first article title and teaser
news_title = soup.find_all('div', class_ = 'content_title')[1].text
news_p = soup.find('div', class_='article_teaser_body').text


print(news_title)
print("------------")
print(news_p)


# JPL Mars Space Images - Featured Image

# In[8]:


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

print(f'featured_image_url = {featured_image_url}')


# Mars Facts

# In[9]:


# URL of page to be scraped
facts_url = 'https://space-facts.com/mars/'
browser.visit(facts_url)

# HTML Object
facts_html = browser.html

# Use Pandas to scrape the table
facts_table = pd.read_html(facts_url)

#facts_table


# In[10]:


# Create dataframe from the correct table
mars_df = facts_table[0]

# Rename columns
mars_df.columns = ['Description','Mars']

# Set Index to be description
mars_df = mars_df.set_index('Description')

mars_df


# In[11]:


# Use Pandas to convert the data to a HTML table string
mars_df.to_html('table.html')


# Mars Hemispheres

# In[12]:


# URL of page to be scraped
mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(mars_url)
main_mars_url = 'https://astrogeology.usgs.gov/'

# HTML Object
mars_html = browser.html

# Parse HTML with Beautiful Soup
mars_soup = bs(mars_html, "html.parser")


# In[13]:


# Create dictionary to store titles & URLs
hemisphere_image_urls = []

# Retrieve all elements that contain image information
mars_path = mars_soup.find_all('div', class_='description')

mars_path


# In[14]:


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
    
hemisphere_image_urls


# In[15]:


browser.quit()


# In[ ]: