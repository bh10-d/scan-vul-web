from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
# URL of the webpage you want to scrape
# url = 'https://0a21007d046732de8003dbbd00790004.web-security-academy.net/'
def scan_url(url):
    visited_urls = set()
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
        if(href.find('/')==0):
            if len(href) != 1:
                print(href)
                convert = href[href.find('/')+1:]
                visited_urls.add(url + convert[:convert.find('=')+1])
                # print(url + convert[:convert.find('=')+1])
                # Print the absolute URL
                # print(absolute_url)
    
    # print(list(visited_urls))

    # return list(visited_urls)

# scan_url('https://0a71008b03b7760d80d8217a0029000d.web-security-academy.net/')