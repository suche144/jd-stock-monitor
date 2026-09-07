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
        print("HTTP：", response.status_code)

        text = response.text.strip()

        if not text:
            print("❌ 接口返回为空")
            return None

        if text.startswith("<"):
            print("❌ 京东返回的是网页，不是库存数据")
            return None

        try:
            data = response.json()
        except Exception:
            print("❌ 返回内容不是 JSON")
            print("返回前200字：", text[:200])
            return None

        item = data.get(str(sku))

        if not item:
            print("⚠️ 没有找到 SKU 库存信息")
            print("返回：", data)
            return None

        state = str(item.get("a", ""))
        quantity = item.get("c", "")

        print("库存状态：", state)
        print("库存数量：", quantity)

        if state == "33":
            print("🔥🔥🔥 有货！")
            bark_push(name, sku, f"有货，库存：{quantity}")
            return True

        if state == "34":
            print("❌ 无货")
            return False

        print("⚠️ 其他库存状态：", state)
        return False

    except Exception as e:
        print("❌ 请求失败：", e)
        return None


def check_stock(name, sku):
    apis = [
        "https://ss.jd.com/ss/areaStockState/mget",
        "https://fts.jd.com/areaStockState/mget",
    ]

    for api in apis:
        result = check_api(name, sku, api)

        if result is not None:
            return result

    print(f"⚠️ {name}：目前两个库存接口都无法正常返回库存数据")
    return None


if __name__ == "__main__":

    print("=" * 60)
    print("京东库存监控启动")
    print("时间：", datetime.now())
    print("监控商品：", len(PRODUCTS))
    print("地区：", AREA)
    print("=" * 60)

    for name, sku in PRODUCTS.items():
        check_stock(name, sku)

    print("=" * 60)
    print("本轮监控结束")
    print("=" * 60)
