import requests
import sys
import time
import detectUrlInContentWebsite as detectUrlInContentWebsite
import payloads


def slowprint(s):
    for c in '\n' + s:
        sys.stdout.write(c)
        sys.stdout.flush()
        # time.sleep(10. / 100)

def sqlinjection(url):
    try:
        def scan(url):
            for payload in payloads.sqlinjection:
                r = requests.get(url + payload)
                if r.status_code == 200:
                    slowprint(
                        f"\033[91m [+] SQL Injection Vulnerability Found In {url+payload}")
                else:
                    slowprint(f"\033[94m [-] Vulnerability Not Found {url+payload}")
                # break

        # Test the scanner with a vulnerable URL
        # url = input("\033[92m [*] Enter URL: ")
        url_list = detectUrlInContentWebsite.scan_url(url)
        # print(url_list)
        for i in range(0, len(url_list)):
            # print(url_list[i])
            # scan(url+''+url_list[i])
            scan(url_list[i])

    except KeyboardInterrupt:
        slowprint("\n [-] Ctrl + C Detected...")
        
    input("\n\033[93m Enter To Exit")
