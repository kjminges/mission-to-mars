# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


### Visit the NASA Mars News Site

# Visit the mars nasa news site
news_url = 'https://redplanetscience.com'
browser.visit(news_url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()


### JPL Space Images Featured Image

# Visit URL
space_img_url = 'https://spaceimages-mars.com'
browser.visit(space_img_url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'


## Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df.to_html()


## Scrape High-Resolution Mars’ Hemisphere Images and Titles
# Hemispheres

# 1. Use browser to visit the URL 
mars_img_url = 'https://marshemispheres.com/'
browser.visit(mars_img_url)

response = requests.get(mars_img_url)
hemi_soup = soup(response.text, 'lxml')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
results = hemi_soup.find_all('div', class_='item')

for result in results:
    
    hemisphere = {}
    
    try:
        hemi_url_rel = result.find('a')['href']
        hemi_url = f'{mars_img_url}{hemi_url_rel}'
        
        browser.visit(hemi_url)
        
        html = browser.html
        img_soup = soup(html, 'html.parser')
        hemi_img_url_rel = img_soup.find('li').find('a').get('href')
        
        hemisphere["image_url"] = f'{mars_img_url}{hemi_img_url_rel}'
        
        browser.back()

        hemisphere["title"] = result.find('h3').text

        hemisphere_image_urls.append(hemisphere)

    except:
        print("-----------------")
        print("Skipping hemisphere")
        print("-----------------")

browser.quit()

