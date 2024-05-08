import requests, re
from bs4 import BeautifulSoup as bs
import config
import access_control_cookie as accesscontrol_cookie
import result


def access_control(url, username="wiener", password="peter"):
    
    def checkRobots(url):
        response = config.r.get(url+"robots.txt")
        if response.status_code == 200:
            disallow = set()
            getDisallow = response.text[response.text.find("Disallow"):].split("Disallow: ")
            for dis in getDisallow:
                if len(dis) != 0:
                    dis = dis.strip()
                    disallow.add(dis)
                    r = requests.get(url+dis.replace("/",""))
                    # print(r.status_code, url+dis.replace("/",""))
                    if r.status_code == 200:
                        # result.result["id"] = 1
                        result.result["vul"] = True
                        result.result["link"] = url+dis.replace("/","")
                        result.result["countPayload"] = 0
                        result.result["payload"] = "None"
                        result.showResult(result.result)
                        # print(result.result)
                        return True
        return False


    def checkContent(url):
        soup = bs(config.s.get(url).content, "html.parser")#config.s
        text = soup.find_all("script")
        pattern = r"setAttribute\('href',\s*'([^']+)'\)"
        for script in text:
            if text != None:
                if script.string != None:
                    # Find all matches of the pattern in the JavaScript code
                    matches = re.findall(pattern, script.string.strip())
                    
                    # Can we use print("admin" in str(text).lower()) to test
                    if "admin" in script.string.strip():
                        response = config.s.get(url+matches[0].replace("/",""))
                        # print(response.status_code, url+matches[0].replace("/",""))
                        result.result["vul"] = True
                        result.result["link"] = url+matches[0].replace("/","")
                        result.result["countPayload"] = 0
                        result.result["payload"] = "None"
                        result.showResult(result.result)
                        # print(result.result)
                        return True
                        return True
        return False
            

    def scan_access_control(url, username, password):
        if checkRobots(url):
            print("[+] Detected robot files")
        elif checkContent(url):
            print("[+] Detected content have admin path using ctrl + u can view")
        elif accesscontrol_cookie.checkCookie(url, username, password):
            print("[+] Detected cookie save status Admin")
        else:
            print("Not Found")

    return scan_access_control(url, username, password)

