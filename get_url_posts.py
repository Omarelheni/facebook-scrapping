import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from utils import extract_fbid_and_create_url
from dotenv import load_dotenv
import os

load_dotenv()


class FacebookURLGetter:
    def __init__(self, username, password, driver_path='/usr/bin/chromedriver'):
        self.username = username
        self.password = password
        self.driver_path = driver_path
        self.driver = self._initialize_driver()
    
    def _initialize_driver(self):
        """Initialize the Chrome WebDriver."""
        ser = Service(self.driver_path)
        options = webdriver.ChromeOptions()
        return webdriver.Chrome(service=ser, options=options)
    
    def login(self):
        """Log into Facebook."""
        self.driver.get('https://www.facebook.com/')
        time.sleep(2)
        email_element = self.driver.find_element(By.ID, 'email')
        password_element = self.driver.find_element(By.ID, 'pass')
        email_element.send_keys(self.username)
        password_element.send_keys(self.password)
        time.sleep(2)
        password_element.submit()
        time.sleep(7)  # Wait for login to complete

    def search_posts(self, topic):
        """Search for posts related to a specific topic."""
        self.driver.get(f'https://www.facebook.com/search/posts/?q={topic}')
        time.sleep(7)
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the page to load more posts."""
        SCROLL_PAUSE_TIME = 1
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        start_time = time.time()
        print('start_time',start_time)
        
        while True:
            end_time = time.time()

            if (end_time - start_time) > 120:  # Stop after 2 minutes
                break
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
    
    def extract_post_links(self):
        anchors = self.driver.find_elements(By.TAG_NAME,'a')
        anchors = [a.get_attribute('href') for a in anchors]

        posts = []
        anchors = [a for a in anchors if '/photo/' in str(a)]

        for a in anchors:
            new_url = extract_fbid_and_create_url(a)
            if new_url is not None:
                posts.append(new_url)
        
        return list(dict.fromkeys(posts))  # Remove duplicates
    
    def save_posts_to_file(self, posts, filename="post_urls.txt"):
        """Save extracted post URLs to a file."""
        with open(filename, "w") as f:
            for post in posts:
                f.write(post + '\n')  # Append a newline character after each post

    
    def close(self):
        """Close the WebDriver."""
        self.driver.quit()

if __name__ == "__main__":

    # Access the variables
    username = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    print(f"Username: {username}, Password: {password}")
    
    scraper = FacebookURLGetter(username, password)
    
    try:
        scraper.login()
        topic = 'uclfinal'
        scraper.search_posts(topic)
        scraper.scroll_to_bottom()
        posts = scraper.extract_post_links()
        print('Extracted posts:', posts)
        scraper.save_posts_to_file(posts)
    finally:
        scraper.close()  # Ensure the driver is closed on completion
