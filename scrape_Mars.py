import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser= init_browser()
#NEWS

    url_news="https://mars.nasa.gov/news/"
    browser.visit(url_news)

    time.sleep(1)

    html_news = browser.html
    soup_news=bs(html_news, 'html.parser')

    news_title=soup_news.find("li", class_="slide").\
        find("div", class_="content_title").text
    news_paragraph=soup_news.find("li", class_="slide").\
        find("div", class_="article_teaser_body").text

#FEATURED IMAGE

    url_image="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    html_image=browser.html
    soup_image=bs(html_image,"html.parser")

    ## Link image jpg
    for link in soup_image.findAll("a",class_="button fancybox"):
        jpg_link=link.get("data-fancybox-href")
    featured_image_url="https://www.jpl.nasa.gov"+jpg_link

    ## Image information
    for info in soup_image.findAll("a",class_="button fancybox"):
        jpg_info=info.get("data-description")
    
    ## Image title
    jpg_title=soup_image.find("h1",class_="media_feature_title").text

#WEATHER

    url_weather="https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather=browser.html
    soup_weather=bs(html_weather,"html.parser")

    mars_weather=soup_weather.find("div", class_="tweet").\
        find("p").text

#FACTS

    url_facts="https://space-facts.com/mars/"
    browser.visit(url_facts)
    html_facts=browser.html
    soup_facts=bs(html_facts,"html.parser")

    facts_df=pd.DataFrame()
    variables=[]
    values=[]
    for rows in soup_facts.findAll("td",class_="column-1"):
        variable=rows.text
        variables.append(variable)

    for rows in soup_facts.findAll("td",class_="column-2"):
        value=rows.text
        values.append(value)

    facts_df["Variable"]=variables
    facts_df["Value"]=values

    html_facts=facts_df.to_html(index=False, border=0)

#HEMISPHERES
    url_hemispheres="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    html_hemispheres=browser.html
    soup_hemispheres=bs(html_hemispheres,"html.parser")
    
    ## Obtaining each individual Hemisphere URL

    hemispheres_urls=[] #Will include all of the individual Hemispheres URLs

    ### Loop to obtain the individual URLs for each Hemisphere

    for link in soup_hemispheres.findAll("a",class_="itemLink product-item"):
        hemisphere_url=link.get("href")
        if "https://astrogeology.usgs.gov"+hemisphere_url not in hemispheres_urls:
            hemispheres_urls.append("https://astrogeology.usgs.gov"+hemisphere_url)
    ## Going through each Hemisphere URL and obtaining Title and Name
    hemispheres_names=[] #Will include each Hemisphere's name
    hemispheres_img_urls=[] #Will include each Hemishpere's image url (jpg)

    for link in hemispheres_urls:

        browser.visit(link)
        html_hemisphere=browser.html
        soup_hemisphere=bs(html_hemisphere,"html.parser")
        
        hemisphere_name=soup_hemisphere.find("h2", class_="title").text
        hemisphere_name=hemisphere_name.replace(" Enhanced","")
        hemispheres_names.append(hemisphere_name)
        
    
        hemisphere_img=soup_hemisphere.find("img", class_="wide-image")
        image=hemisphere_img.get("src")
        hemispheres_img_urls.append("https://astrogeology.usgs.gov"+image)
    
    ## Saving as a Dictionary
    hemisphere_dicts=[] # Will group the hemispheres dictionary
    
    
    ###Loops through each image and name to store it as a dictionary
    for i in range(len(hemispheres_img_urls)):
        hemisphere_dict={}
        hemisphere_dict["title"]=hemispheres_names[i]
        hemisphere_dict["image"]=hemispheres_img_urls[i]
        hemisphere_dict["url"]=hemispheres_urls[i]
        hemisphere_dicts.append(hemisphere_dict)
    
# Store data in a dictionary
    mars={
        "latest_news_t":news_title,
        "latest_news_p":news_paragraph,
        "featured_img":featured_image_url,
        "featured_img_title":jpg_title,
        "featured_img_info":jpg_info,
        "weather_tweet":mars_weather,
        "facts":html_facts,
        "hemispheres":hemisphere_dicts,
    }

    browser.quit()

    return mars