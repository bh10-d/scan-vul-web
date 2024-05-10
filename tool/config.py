import requests
from bs4 import BeautifulSoup as bs


#request lib pure
r = requests

#request through session
s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
# s.headers["Connection"] = "close"
# s.headers["Cache-Control"] = "no-cache"