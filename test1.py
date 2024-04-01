from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
# URL of the webpage you want to scrape
url = 'https://0add00050435a9068146c07300d400d5.web-security-academy.net/'
# Send an HTTP request to the URL
response = requests.get(url)
response.raise_for_status()  # Raise an error for bad responses
# Parse the webpage content
soup = BeautifulSoup(response.text, 'html.parser')
# Find all the 'a' tags on the webpage
for a_tag in soup.find_all('a'):
    # Get the href attribute from the 'a' tag
    href = a_tag.get('href')
    # Use urljoin to convert the relative URL to an absolute URL
    absolute_url = urljoin(url, href)
    # Print the absolute URL
    print(absolute_url)