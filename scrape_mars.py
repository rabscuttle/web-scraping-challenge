# Import
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser

def scrape():
    # Mars News
    url1 = 'https://mars.nasa.gov/news'
    response = requests.get(url1)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find(class_='content_title').text.strip()
    news_p = soup.find(class_='rollover_description_inner').text.strip()
    
    # JPL
    base_url = 'https://www.jpl.nasa.gov'
    url2 = f'{base_url}/spaceimages/?search=&category=Mars'

    executable_path = {'executable_path':'C:/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = True)
    browser.visit(url2)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find(class_='button fancybox')["data-fancybox-href"]
    browser.quit()

    featured_image_url = f'{base_url}{featured_image_url}'
    featured_image_url
    
    # Mars Facts
    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)
    facts_df = tables[0]
    facts_df.set_index(0, inplace=True)
    facts_df.to_html('mars_facts.html')

    html_file = open('mars_facts.html' , 'r')
    table_html = html_file.read() 
    table_html = table_html.replace('\n', '')
    body = table_html.find('<tbody>')
    final_html = table_html[body:]
    
    # Mars Hemispheres
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    executable_path = {'executable_path':'C:/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = True)
    browser.visit(url4)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all(class_='description')

    # Variables
    hemisphere_image_urls = []

    for result in results:
        link = 'https://astrogeology.usgs.gov' + result.find('a')['href']
        executable_path = {'executable_path':'C:/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless = True)
        browser.visit(link)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
   
        # Title
        title = soup.find(class_='title').text.strip()
        title = title.replace('Enhanced','')
        title = title.strip()
 
        # Link
        img = soup.find(class_='downloads')
        img_url = img.find('a')['href']
    
        dict = {'title':title, 'img_url':img_url}
        hemisphere_image_urls.append(dict)
        browser.quit()

    browser.quit()
    
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls,
        "mars_facts": final_html
    }

    return mars_data