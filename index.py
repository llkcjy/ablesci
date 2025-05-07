import os
import requests
from ablesci import ablesci

# 从环境变量获取 Cookie 和 Server酱的SCKEY
Cookie = os.environ.get("SITE_TOKEN")
SERVER_JANG_SCKEY = os.environ.get("SERVER_JANG_SCKEY")

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": f"{Cookie}",
    "DNT": "1",
    "Referer": "https://www.ablesci.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

def send_server_jiang(title, message):
    """通过Server酱发送通知"""
    if not SERVER_JANG_SCKEY:
        print("未配置SERVER_JANG_SCKEY环境变量，无法发送通知")
        return

    url = f"https://sctapi.ftqq.com/{SERVER_JANG_SCKEY}.send"
    data = {
        "title": title,
        "desp": message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # 检查HTTP请求是否成功
        print("Server酱通知发送成功")
    except Exception as e:
        print(f"Server酱通知发送失败: {str(e)}")

def main():
    try:
        ablesci(headers=headers)
    except Exception as e:
        error_msg = f"ablesci执行失败，错误信息: {str(e)}"
        print(error_msg)
        send_server_jiang("Ablesci任务异常", error_msg)

if __name__ == "__main__":
    main()
