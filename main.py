from facebook_scraper import get_posts, set_user_agent
import pymongo

# Set a custom user agent
set_user_agent("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["facebook_scraping"]  # Renamed database for clarity
posts_collection = db["posts"]

print("Starting Facebook scraping process...")


# Read post URLs from a file
with open("post_urls.txt") as file:
    post_urls = [line.strip() for line in file]  # Remove newline characters

# Fetch posts from the list of URLs
post_generator = get_posts(
    post_urls=post_urls,
    options={"comments": 50, "progress": True}
)

# Process each post
for post_data in post_generator:
    print("Processing post...")

    # Keys to keep from the post
    desired_post_keys = ['text', 'images', 'username', 'comments', 'comments_full']
    filtered_post = {key: post_data[key] for key in desired_post_keys if key in post_data}

    # Process and filter comments
    comment_keys = ["commenter_name", "comment_text"]
    processed_comments = []
    for comment in filtered_post.get('comments_full', []):
        processed_comment = {key: comment[key] for key in comment_keys if key in comment}
        processed_comments.append(processed_comment)

    # Update the filtered post with processed comments
    filtered_post['comments_full'] = processed_comments

    # Insert the processed post into MongoDB
    insert_result = posts_collection.insert_one(filtered_post)
    print("Document inserted with ID:", insert_result.inserted_id)

print("Scraping process completed.")
