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
    news_p=soup_news.find("li", class_="slide").\
        find("div", class_="article_teaser_body").text

#FEATURED IMAGE

    url_image="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    html_image=browser.html
    soup_image=bs(html_image,"html.parser")

    for link in soup_image.findAll("a",class_="button fancybox"):
        jpg_link=link.get("data-fancybox-href")
    featured_image_url="https://www.jpl.nasa.gov"+jpg_link

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

    html_facts=facts_df.to_html()

#HEMISPHERES
    url_hemispheres="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)
    html_hemispheres=browser.html
    soup_hemispheres=bs(html_hemispheres,"html.parser")

    hemispheres_img=[]
    hemispheres_names=[]
    hemisphere_img_urls=[]

    for link in soup_hemispheres.findAll("a",class_="itemLink product-item"):
        hemisphere_img=link.get("href")
        if "https://astrogeology.usgs.gov"+hemisphere_img in hemispheres_img:
            hemispheres_img
        else:
            hemispheres_img.append("https://astrogeology.usgs.gov"+hemisphere_img)

    for name in soup_hemispheres.findAll("h3"):
        hemispheres_names.append(name.text)

    for x in range(len(hemispheres_names)):
        hemisphere_img_urls.append({"title":hemispheres_names[x],"img_url":hemispheres_img[x]})

# Store data in a dictionary
    mars={
        "latest_news_t":news_title,
        "latest_news_p":news_p,
        "featured_img":featured_image_url,
        "weather_tweet":mars_weather,
        "facts":html_facts,
        "hemispheres":hemisphere_img_urls
    }

    browser.quit()

    return mars