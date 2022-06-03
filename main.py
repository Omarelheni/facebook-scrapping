from facebook_scraper import get_posts
from facebook_scraper import *
import pymongo


set_user_agent(
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["facebookscraping"]

mycol = mydb["posts"]


#ourvir le fichier post_urls pour obtenir les urls
with open('post_urls.txt') as f:
    #supprimer les \n
    lines =[ a.replace('\n', '') for a in f.readlines() ]
    for post in get_posts(options={"comments": True},post_urls = lines):

        #supprimer les clés qui no sont pas necessaire
        your_keys = ['text','images','username','comments','comments_full']
        post = { your_key: post[your_key] for your_key in your_keys }
        your_keys = ["commenter_name","comment_text"]
        com_l = []
        for com in post['comments_full']:
            com = { your_key: com[your_key] for your_key in your_keys }
            com_l.append(com)
        post['comments_full']= com_l

        #insert a document to the collection
        x = mycol.insert_one(post)
        #id returned by insert_one
        print("Document inserted with id: ", x.inserted_id)

        
        
