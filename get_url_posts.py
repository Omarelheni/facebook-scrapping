import time,random
import os
from bs4 import BeautifulSoup
from selenium import  webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from urllib.request import urlretrieve


# instancier l'objet du webdriver
ser = Service("chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)
driver.get('https://www.facebook.com/')
#Connexion
file = open('config')
lines = file.readlines()
username = lines[0]
password = lines[1]
elementIDP = driver.find_element(By.ID,'pass')
elementIDE = driver.find_element(By.ID,'email')
elementIDP.send_keys(password)
elementIDE.send_keys(username)
time.sleep(7)

#selection du sujet 
topic = 'uclfinal'
#recherche
driver.get('https://www.facebook.com/search/posts/?q='+ topic)
time.sleep(7)

#Scrolling
SCROLL_PAUSE_TIME = 1

last_height = driver.execute_script("return document.body.scrollHeight")
start = time.time()

while True:
    end = time.time()
    if (end - start > 120):
        break 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
 
    last_height = new_height

#get the links
anchors = driver.find_elements(By.TAG_NAME,'a')
anchors = [a.get_attribute('href') for a in anchors]

#réduire tous les liens vers des liens d'images uniquement puisque c'est le seul endroit
#où j'aurais pu trouver l'url du publication
posts = []
anchors = [a for a in anchors if '/photos/pcb.' in str(a)]

for a in anchors:
    pos2 = ( [pos for pos, char in enumerate(a) if char == '/'])[5]
    pos1 = ( [pos for pos, char in enumerate(a) if char == '.'])[2]
    post = a[(pos1 + 1) : pos2]
    posts.append(post)
posts = list(dict.fromkeys(posts))

#enregistrer les urls dans un fichier
for a in posts:
    with open("post_urls.txt", "a") as f:
        f.write('https://www.facebook.com/'+a)
        f.write('\n')
        f.close()
