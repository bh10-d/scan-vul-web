# import requests
import sys
import time
import detectUrlInContentWebsite as detectUrlInContentWebsite
import config
import payloads



def slowprint(s):
    for c in '\n' + s:
        sys.stdout.write(c)
        sys.stdout.flush()
        # time.sleep(10. / 100)

def sqlinjection(url):
    def scan(url):
        for payload in payloads.sqlinjection:
            r = config.r.get(url + payload)
            if r.status_code == 200:
                slowprint(
                    f"\033[91m [+] SQL Injection Vulnerability Found In {url+payload}")
            else:
                slowprint(f"\033[94m [-] Vulnerability Not Found {url+payload}")

    url_list = detectUrlInContentWebsite.scan_url(url)
    for i in range(0, len(url_list)):
        scan(url_list[i])
