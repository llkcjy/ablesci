# -*- coding: utf-8 -*-
import requests
import json
import os
import time

MAX_RETRY = 3

def parse_cookies(cookie_str):
    cookies = {}
    for part in cookie_str.split(';'):
        if '=' in part:
            k, v = part.strip().split('=', 1)
            cookies[k] = v
    return cookies

def send_server_chan(title, message, server_chan_key):
    if not server_chan_key:
        print('[WARN] 未配置 Server 酱 key，跳过通知')
        return
    url = f"https://sc.ftqq.com/{server_chan_key}.send"
    try:
        data = {
            "text": title.encode('utf-8'),
            "desp": message.encode('utf-8')
        }
        resp = requests.post(url, data=data, timeout=10)
        print("[INFO] Server酱返回:", resp.text)
    except Exception as e:
        print("[ERROR] Server酱发送失败:", str(e))

def checkin(cookie_str, server_chan_key):
    url = "https://2o.riolu.sbs/skyapi?action=checkin"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://2o.riolu.sbs/dashboard"
    }
    cookies = parse_cookies(cookie_str)

    for attempt in range(1, MAX_RETRY + 1):
        try:
            resp = requests.get(url, headers=headers, cookies=cookies, timeout=10)  # ✅ 正确为 GET
            result = json.loads(resp.content)
            if result.get("code") == 0:
                msg = u"[成功] 签到完成：" + result.get("message", "")
                print(msg)
                send_server_chan("VPN签到成功", msg, server_chan_key)
                return
            else:
                msg = u"[业务失败] " + result.get("message", "未知错误")
                print(msg)
                send_server_chan("VPN签到失败", msg, server_chan_key)
                return
        except Exception as e:
            print("[第{}次尝试] 网络异常：{}".format(attempt, str(e)))
            time.sleep(2)

    send_server_chan("VPN签到失败", "超过最大重试次数，签到失败", server_chan_key)

if __name__ == "__main__":
    COOKIE_LADDER_STR = os.environ.get("COOKIE_LADDER_STR")
    SERVER_JANG_SCKEY = os.environ.get("SERVER_JANG_SCKEY")
    if not COOKIE_LADDER_STR:
        print("[ERROR] COOKIE_STR 未设置")
    else:
        checkin(COOKIE_LADDER_STR, SERVER_JANG_SCKEY)
