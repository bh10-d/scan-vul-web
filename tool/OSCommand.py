import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import certifi  # Import certifi to manage SSL certificates
import result

# Khởi tạo colorama
init(autoreset=True)

def load_keywords(file_path):
    """ Hàm để đọc các từ khoá từ một tệp. """
    with open(file_path, "r") as file:
        return [line.strip().lower() for line in file]

def interact_with_form(url, verify_ssl=True):
    payloads = open("payloads/payload-OSCommand.txt", "r")  # Danh sách các payload để thử
    keywords = load_keywords("payloads/list-OSCommand.txt")  # Đọc từ khoá từ tệp
    ssl_cert = certifi.where() if verify_ssl else False  # Determine SSL certificate based on verify_ssl flag

    try:
        # Gửi yêu cầu GET để lấy trang web
        response = requests.get(url, verify=ssl_cert)
        response.raise_for_status()

        # Phân tích HTML bằng BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tìm tất cả thẻ input và textarea
        form_elements = soup.find_all(['input', 'textarea'])

        # Lặp qua từng payload trong danh sách các payload
        for payload in payloads:
            payload = payload.strip()
            data_to_post = {}
            # print(f"{Fore.YELLOW}Testing payload: {payload}")
            for element in form_elements:
                element_name = element.get('name', 'unnamed_element')
                element_type = element.name
                if element_name == "csrf":
                    # Sử dụng giá trị hiện tại cho input có name="csrf"
                    csrf_value = element.get('value')
                    data_to_post[element_name] = csrf_value
                    # print(f"{Fore.CYAN}{element_type}[name={element_name}]: {csrf_value} (preserved)")
                else:
                    # Gán payload vào các input và textarea
                    data_to_post[element_name] = payload
                    # print(f"{Fore.MAGENTA}{element_type}[name={element_name}]: {payload}")

            # Gửi yêu cầu POST với dữ liệu payload hiện tại
            post_response = requests.post(url, data=data_to_post, verify=ssl_cert)
            # print(f"POST response status code: {post_response.status_code}")

            # Phân tích phản hồi từ server
            response_text_lower = post_response.text.lower()
            if any(keyword in response_text_lower for keyword in keywords):
                result.result['vul'] = True
                result.result['link'] = url
                result.result['payload'] = payload
                result.listObject(result.result)
                # result.showResult()
                # print(f"{Fore.RED}Possible successful command injection detected based on keyword match!")
                # print("------------------------------------------------------------------------------------")
            # else:
            #     print(f"{Fore.GREEN}No matches found with the specified keywords in the response.")
            #     print("------------------------------------------------------------------------------------")
        result.showResult()
    except requests.RequestException as e:
        print(f"{Fore.RED}Error interacting with the URL {url}: {e}")
    finally:
        payloads.close()

# Example usage with SSL verification enabled
# interact_with_form("https://sinhvien.ufl.udn.vn/DangNhap/Login",  verify_ssl=False)
# interact_with_form("http://192.168.1.9/OS%20command%20Lab%203/", verify_ssl=False)
# interact_with_form("http://192.168.1.3/", verify_ssl=False)
# interact_with_form("https://elearning2.vku.udn.vn/login/index.php", verify_ssl=False)