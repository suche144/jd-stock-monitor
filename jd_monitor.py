import os
import requests
from datetime import datetime

PRODUCTS = {
    "花朵系列": "10217041125002",
    "水果系列": "10196364421727",
    "花的礼物": "10234330610956",
    "小食系列": "10194711794453",
    "海洋系列": "10206630653783",
    "甜点系列": "10204591360228",
}

AREA = os.getenv("JD_AREA", "19_1607_0_0")
BARK_KEY = os.getenv("BARK_KEY")


def bark_push(name, sku, stock):
    if not BARK_KEY:
        print("⚠️ BARK_KEY 尚未配置，跳过推送")
        return

    url = f"https://api.day.app/{BARK_KEY}"

    data = {
        "title": "🔥 京东库存提醒",
        "body": f"{name}\n库存状态：{stock}\nSKU：{sku}",
        "url": f"https://item.jd.com/{sku}.html",
    }

    try:
        r = requests.post(url, json=data, timeout=10)
        print("Bark 推送状态：", r.status_code)
    except Exception as e:
        print("Bark 推送失败：", e)


def check_api(name, sku, api_url):
    params = {
        "app": "cart_pc",
        "ch": "1",
        "skuNum": f"{sku},1",
        "area": AREA.replace("_", ","),
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Referer": "https://cart.jd.com/",
        "Accept": "application/json,text/plain,*/*",
    }

    try:
        response = requests.get(
            api_url,
            params=params,
            headers=headers,
            timeout=15,
        )

        print(f"\n{name} | SKU：{sku}")
        print("接口：", api_url)
        print("HTTP：", response.sta
    p("本轮监控结束")
    print("=" * 60)
