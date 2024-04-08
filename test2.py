import requests
import sys
import time

def scan(url):
    
    payloads = open("list.txt","r")
    for payload in payloads:
        # time.sleep(10. / 100)
        response = requests.get(url+payload)
        print(f'statusCode: {response.status_code} - url: {url+payload}')
    # for payload in payloads:
    #     r = requests.get(url + payload)
    #     if r.status_code == 200:
    #         slowprint(
    #             f"\033[91m [+] SQL Injection Vulnerability Found In {url}")
    #     else:
    #         slowprint(f"\033[94m [-] Vulnerability Not Found {url}")
    #     break

url = "http://localhost:3000/"
scan(url)



# from bs4 import BeautifulSoup

# url = "https://0aac004f049162808029df8a002e00ce.web-security-academy.net/"

# response = requests.get(url)
# soup = BeautifulSoup(response.content, "html.parser")

# # Tìm kiếm thẻ meta có tên generator
# generator_meta = soup.find("meta", {"name": "generator"})

# # Tìm kiếm thẻ meta có tên content
# content_meta = soup.find("meta", {"name": "content"})

# if generator_meta:
#     print("Generator:", generator_meta["content"])

# if content_meta:
#     print("Content:", content_meta["content"])