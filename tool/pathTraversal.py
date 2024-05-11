import requests
from colorama import Fore, Style, init
import result

# Khởi tạo colorama
init(autoreset=True)

def run_path_traversal_scan(base_url):
    def read_payloads(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]

    def analyze_content(content, vulnerability_signatures):
        for signature in vulnerability_signatures:
            if signature in content:
                return f"{Fore.RED}Phát hiện chuỗi '{signature}' trong phản hồi, chỉ ra khả năng có lỗ hổng."
        return None

    # Tên các file đã được định sẵn trong hàm và đường dẫn đã được chỉnh sửa
    param_file = 'payloads/payloadParam.txt'  # Chỉnh sửa đường dẫn file này
    payload_file = 'payloads/payloadPath.txt'
    signature_file = 'payloads/payloadResult.txt'

    # Đọc dữ liệu từ file
    path_traversal_payloads = read_payloads(payload_file)
    vulnerability_signatures = read_payloads(signature_file)

    # Đọc và áp dụng từng tham số từ file param_file
    with open(param_file, 'r', encoding='utf-8') as file:
        for param_name in file:
            param_name = param_name.strip()
            if param_name:
                for payload in path_traversal_payloads:
                    attack_url = f"{base_url}?{param_name}={payload}"
                    try:
                        response = requests.get(attack_url)
                        if response.status_code == 200:
                            sensitive_data = analyze_content(response.text, vulnerability_signatures)
                            if sensitive_data:
                                result.isPathTraversal = True
                                result.result['vul'] = True
                                result.result['link'] = attack_url
                                result.result['payload'] = payload
                                result.result['param'] = param_name
                                result.listObject(result.result)
                                # print(f"Đang kiểm tra payload: {payload}")
                                # print(f"URL: {attack_url}")
                                # print(f"Mã trạng thái: {response.status_code}")
                                # print("!!! Phát hiện khả năng có lỗ hổng điều hướng đường dẫn !!!")
                                # print(f"{Fore.RED}Dữ liệu nhạy cảm tìm thấy trong phản hồi:", sensitive_data)
                                # print("\n" + "="*50 + "\n")
                    except requests.RequestException as e:
                        print(f"Không thể kết nối đến {attack_url}. Lỗi: {e}")
        if len(result.array) != 0:
            result.showResult()
        else:
            print("Deso cos casi looix loonf naof car")
# base_url = "http://192.168.1.104/Path%20Traversal/read_poem_web/index.php"
# base_url = "http://192.168.1.3/index.php"

# run_path_traversal_scan("http://192.168.1.3/index.php")