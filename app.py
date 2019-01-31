from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrapy_mars import scrape
import os

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_db"


str0=os.environ.get("MONGODB_URI")
# str0="mongodb://localhost:27017/Mars_db"

str1=str0.split('/');   Mars_db=str1[-1];
str0='/'.join(str1)
app.config["MONGO_URI"]=str0

mongo = PyMongo(app)


mongo.db.drop_collection ("Mars_hemisphere_image_urls")
mongo.db.drop_collection ("Mars_facts_dict")
mongo.db.drop_collection ("Mars_weather")
mongo.db.drop_collection ("Mars_latest_news")
mongo.db.drop_collection ("Mars_featured_image_url")


# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
   # listings = mongo.db.Mars.find_one()
   

    # hemisphere_image_urls=mongo.db.Mars_hemisphere_image_urls.find()
    # hemisphere_image_urls=[result for result in hemisphere_image_urls]

    # try:
    #     hemisphere_image_urls12=hemisphere_image_urls[:2]
    # except:
    #     hemisphere_image_urls12=[]

    # try:
    #     hemisphere_image_urls34=hemisphere_image_urls[-2:]
    # except:
    #     hemisphere_image_urls34=[]

    facts_dict=mongo.db.Mars_facts_dict.find()
    try: 
        facts_dict=facts_dict[0]
    except:
        facts_dict={}


    # facts_dict_keys  = mongo.db.Mars_facts_dict_keys.find()
   
    # facts_dict_values= mongo.db.Mars_facts_dict_keys_values.find()    


    weather=mongo.db.Mars_weather.find()
    try: 
        weather=weather[0]
    except:
        weather=[]

    latest_news=mongo.db.Mars_latest_news.find()
    try: 
        latest_news=latest_news[0]
    except:
        latest_news=[]


    featured_image_url=mongo.db.Mars_featured_image_url.find()
    try: 
        featured_image_url=featured_image_url[0]
    except:
        featured_image_url=[]

    #from constants import hemisphere_image_urls,facts_dict,facts_dict_keys,facts_dict_values,weather,latest_news,featured_image_url
    #from constants import hemisphere_image_urls


    x=list(zip(list(facts_dict.keys())[1:],list(facts_dict.values())[1:]))
    return render_template("index.html",\
    #hemisphere_image_urls34=hemisphere_image_urls34,\
        facts_dict=facts_dict,weather=weather,\
        x=x, latest_news=latest_news,featured_image_url=featured_image_url,\
        #hemisphere_image_urls12=hemisphere_image_urls12
        )



@app.route("/scrape")
def scraper():
    scrape()
    # listings = mongo.db.listings
    # listings_data = scrape()
    # listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)