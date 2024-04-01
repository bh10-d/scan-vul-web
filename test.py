import requests
import re
import sys
import time

def waiting():
    waiting = ' Waiting...'
    sys.stdout.write('\r')
    sys.stdout.flush()
    for c in waiting:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(10. / 100)
        

def scan_url(url):
    # Tạo bộ sưu tập để lưu trữ URL đã quét
    visited_urls = set()
    test_urls = set()
    # Tạo hàng đợi để lưu trữ URL chờ quét
    queue = [url]

    # Duyệt qua các URL trong hàng đợi
    while queue:
        waiting()
        # Lấy URL đầu tiên trong hàng đợi
        current_url = queue.pop(0)

        # Kiểm tra nếu URL đã được quét
        if current_url in visited_urls:
            continue

        # Thêm URL vào danh sách đã quét
        visited_urls.add(current_url)

        # In URL
        # print(re.sub(r"(//)(.*?)(//)", r"\1/\3", current_url))
        test = current_url.split("//")
        # print(current_url.replace("//", "/"))
        # print(current_url)
        if len(test) == 2:
            test_urls.add(test[1])
            # print(test[1])
        else:
            test_urls.add(test[2])
            # print(test[2])
            

        # Lấy nội dung trang web
        response = requests.get(current_url)

        # Tìm kiếm các liên kết trong nội dung trang web
        for link in response.text.split('"'):
            # Xử lý các liên kết tương đối
            if link.startswith("/") and not link.startswith("//"):
                # Xác định URL đầy đủ
                full_url = f"{url}{link}"

                # Thêm URL mới vào hàng đợi
                if full_url not in visited_urls:
                    queue.append(full_url)
    # convert = list(visited_urls)
    # for i in range(0, len(convert)-1):
    #     visited_urls.add(convert[i].replace("//", "/"))
    return list(test_urls)


# Ví dụ sử dụng
# url = "https://0a1800a504280cf384d3730400320095.web-security-academy.net/"
# scan_url(url)
# print(scan_url(url))
