from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import pandas as pd

description=[]
value = []

urls={
"Hemisphere_Name":[], 
"Enahnced_URL":[], 
"Full_Image URL":[]
}

hemisphere_urls=[]

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Scrape internet to obtain the latest headline and article for mars news 
    article_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest/'
    browser.visit(article_url)

    html = browser.html
    soup = bs(html, "html.parser")

    article_title = soup.find_all(class_='content_title')

    latest_news_title=[]
    for x in article_title:
        news_title=x.find("a").text
        latest_news_title.append(news_title)

    latest_article_title=latest_news_title[0]

    article_body=soup.find_all(class_="article_teaser_body")
    latest_news_body=article_body[0].text

    # Close the browser after scraping
    browser.quit()

    #Scrape internet for mars feature image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    feature_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(feature_image_url)

    html = browser.html
    soup = bs(html, "html.parser")

    feature_image = soup.find_all(class_='carousel_container')

    feature_image1 = feature_image[0].find('a')["data-fancybox-href"]
    feature_image1 = feature_image1.split("/")
    feature_image2 = "/"+feature_image1[2]+"/"+"largesize"+"/"+feature_image1[4]
    feature_image2=feature_image2[:-6]

    feature_link="https://www.jpl.nasa.gov/spaceimages"+feature_image2+"hires.jpg"

    # Close the browser after scraping
    browser.quit()

    #Scrape internet for mars weather data from twitter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    
    html = browser.html
    soup = bs(html, "html.parser")

    weather=soup.find_all(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    weather_text=weather[0].text

    # Close the browser after scraping
    browser.quit()

    #Scrape internet for a table of mars facts
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_data_url = 'https://space-facts.com/mars/'
    browser.visit(mars_data_url)

    html = browser.html
    soup = bs(html, "html.parser")

    table_data=soup.find_all(class_="tablepress tablepress-id-mars")
    table_rows=table_data[0].find_all('tr')
    
    for x in range(len(table_rows)):
        description.append(table_rows[x]('td')[0].text)
        value.append(table_rows[x]('td')[1].text)

    df=pd.DataFrame(list(zip(description, value)),columns=['Description','Value'])
    df=df.set_index('Description')

    fact_table=df.to_html()

    # Close the browser after scraping
    browser.quit()

    #Scrape internet for a images of mars hemispheres
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    enahnced_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(enahnced_url)

    html = browser.html
    soup = bs(html, "html.parser")

    pics_title=soup.find_all(class_="description")
    
    for urlss in pics_title:
        print(urlss)
    
    for x in range(len(pics_title)):
        urls["Hemisphere_Name"].append(pics_title[x]('a')[0].text)
        urls["Enahnced_URL"].append(("https://astrogeology.usgs.gov/"+pics_title[x]('a')[0]["href"]))

    for pic_url in urls["Enahnced_URL"]:
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(pic_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        urls["Full_Image URL"].append(soup.find_all(class_="downloads")[0]("li")[0]('a')[0]["href"])
        browser.quit()

    for x in range(len(urls)+1):
        info={
        "title":urls["Hemisphere_Name"][x], 
        "image_url":urls["Full_Image URL"][x]
        }
        print(x)
        print(info)
        hemisphere_urls.append(info)


    # Close the browser after scraping
    browser.quit()

    html_data = {
        "latest_article_title": latest_article_title,
        "latest_news_body": latest_news_body,
        "feature_link": feature_link,
        "weather_text": weather_text,
        "fact_table":fact_table, 
        "hemisphere_urls": hemisphere_urls
        }
    
    # Return results
    return html_data