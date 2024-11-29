import re

def extract_fbid_and_create_url(original_url):
    # Use regex to find the fbid in the original URL
    match = re.search(r'fbid=(\d+)', original_url)
    if match:
        fbid = match.group(1)  # Extract the fbid
        # Create the new URL
        new_url = f'https://www.facebook.com/photo/?fbid={fbid}'
        return new_url
    else:
        return None