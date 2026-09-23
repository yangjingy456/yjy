#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可口可乐小程序 - 独立签到脚本
"""
import os
import sys
import json
import requests
from datetime import datetime

# ====== 从环境变量读取 Token ======
# 青龙面板 → 环境变量 中设置 wx_auth
TOKEN = os.environ.get("wx_auth", "")

if not TOKEN:
    print("❌ 未找到环境变量 wx_auth，请在青龙面板的环境变量中添加！")
    sys.exit(1)

URL = "https://member-api.icoke.cn/api/icoke-sign/icoke/mini/sign/main/sign"

def sign_in():
    headers = {
        "Authentication": TOKEN,
        "Accept": "application/json, text/plain, */*",
        "Host": "member-api.icoke.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B)",
    }

    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if data.get("isSuccess") or data.get("success"):
            print(f"✅ [{now}] 签到成功！获得 {data.get('point', 0)} 积分")
            print(f"   返回信息: {data.get('message', '')}")
        else:
            print(f"⚠️  [{now}] 签到失败: {data.get('message', '未知错误')}")

        return True

    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络")
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
    except json.JSONDecodeError:
        print(f"❌ 返回数据解析失败，原始内容: {response.text}")

    return False

if __name__ == "__main__":
    print("=" * 45)
    print("  可口可乐小程序 - 每日自动签到")
    print(f"  Token 长度: {len(TOKEN)} 字符")
    print("=" * 45)
    sign_in()

