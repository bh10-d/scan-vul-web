# from bs4 import BeautifulSoup
# import requests
# from urllib.parse import urljoin
# # URL of the webpage you want to scrape
# def scan_url(url):
#     visited_urls = set()
#     # Send an HTTP request to the URL
#     response = requests.get(url)
#     response.raise_for_status()  # Raise an error for bad responses
#     # Parse the webpage content
#     soup = BeautifulSoup(response.text, 'html.parser')
#     # Find all the 'a' tags on the webpage
#     for a_tag in soup.find_all('a'):
#         # Get the href attribute from the 'a' tag
#         href = a_tag.get('href')
#         # print(href)
#         # Use urljoin to convert the relative URL to an absolute URL
#         absolute_url = urljoin(url, href)
#         if(href.find('/')==0):
#             if len(href) != 1:
#                 convert = href[href.find('/')+1:]
#                 print(convert[:convert.find('=')+1])
#                 if '=' in convert:
#                     visited_urls.add(url + convert[:convert.find('=')+1])
#                 else:
#                     visited_urls.add(url + convert)
#                 # print(visited_urls)
    
#     print(list(visited_urls))

# scan_url('http://localhost:3000/')


import requests

def check_redirect(url):
  """
  This function checks if a URL redirects and returns the final destination URL.
  """
  try:
    response = requests.get(url, allow_redirects=False)  # Don't follow redirects
    response.raise_for_status()  # Raise error for non-2xx status codes

    # Check for redirect status codes (3xx)
    if response.history:
      last_response = response.history[-1]
      if last_response.status_code >= 300 and last_response.status_code <= 399:
        return last_response.url  # Return the final redirected URL
    else:
      return url  # No redirection

  except requests.exceptions.RequestException as e:
    print(f"Error processing {url}: {e}")
    return None

# Example usage
url = "http://localhost:3000/login"  # Can be a redirected URL
redirected_url = check_redirect(url)
if redirected_url:
  print(f"Original URL: {url}")
  print(f"Redirected URL: {redirected_url}")
else:
  print(f"URL {url} is not redirected.")