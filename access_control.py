import requests, re
from bs4 import BeautifulSoup as bs
# from urllib.parse import urljoin
# from pprint import pprint
import access_control_cookie as accesscontrol_cookie

# buoc dau tien se detect robots.txt

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
# soup = bs(s.get("http://localhost:3000/lab1/robots.txt").content, "html.parser")

# print(soup)




def access_control(url):
    try:
        def checkRobots(url):
            # response = requests.get("http://localhost:3000/lab1/robots.txt")
            response = requests.get(url+"robots.txt")
            # print(response.status_code)
            if response.status_code == 200:
                # print(f"\033[92m[+] http://localhost:3000/lab1/robots.txt detected")
                disallow = set()
                # print(test.split("Disallow: "))
                # disallow.add(response.text[response.text.find("Disallow"):])
                # disallow.add(response.text[response.text.find("Disallow"):])
                getDisallow = response.text[response.text.find("Disallow"):].split("Disallow: ")
                # print(getDisallow[1 ])
                for dis in getDisallow:
                    if len(dis) != 0:
                        dis = dis.strip()
                        disallow.add(dis)
                        # print("\\" in dis)
                        # string = handleString(dis)
                        # print(string)
                        # print(list(string))
                        r = requests.get(url+dis.replace("/",""))
                        # print(dis.replace("/",""))
                        # print("http://localhost:3000/lab1"+string)
                        print(r.status_code, url+dis.replace("/",""))
                        if r.status_code == 200:
                            return True
            return False


        def checkContent(url):
            # print("alive")
            soup = bs(s.get(url).content, "html.parser")
            # print(response.text)
            text = soup.find_all("script")
            pattern = r"setAttribute\('href',\s*'([^']+)'\)"
            # print(text)
            for script in text:
                # if "admin" in script.string.lower():

                    if text != None:
                        if script.string != None:
                            # Find all matches of the pattern in the JavaScript code
                            matches = re.findall(pattern, script.string.strip())
                            
                            # Can we use print("admin" in str(text).lower()) to test
                            if "admin" in script.string.strip():
                                # response = requests.get(url+matches[0].replace("/",""))
                                response = s.get(url+matches[0].replace("/",""))
                                print(response.status_code, url+matches[0].replace("/",""))
                                return True
            return False
                

        # checkRobots()
        # checkContent()
        def scan_access_control(url):
            if checkRobots(url):
                print("[+] Detected robot files")
            elif checkContent(url):
                print("[+] Detected content have admin path using ctrl + u can view")
            elif accesscontrol_cookie.checkCookie(url):
                print("[+] Detected cookie save status Admin")
            else:
                print("Not Found")

        return scan_access_control(url)

    except KeyboardInterrupt:
        print("Exiting...")
		# slowprint("\n\033[91m [-] Exiting...")
	# return detect_form
