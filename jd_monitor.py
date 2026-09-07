import os
import requests
from datetime import datetime

# =========================
# 京东商品监控列表
# =========================

PRODUCTS = {
    "花朵系列": "10217041125002",
    "水果系列": "10196364421727",
    "花的礼物": "10234330610956",
    "小食系列": "10194711794453",
    "海洋系列": "10206630653783",
    "甜点系列": "10204591360228",
}

# =========================
# Bark Key
# 从 GitHub Secrets 中读取
# =========================

BARK_KEY = os.getenv("BARK_KEY")

# 深圳地区
AREA = os.getenv("JD_AREA", "19_1607_0_0")


def bark_push(title, content):
    """发送 Bark 通知"""

    if not BARK_KEY:
        print("错误：没有配置 BARK_KEY")
        return

    url = f"https://api.day.app/{BARK_KEY}"

    params = {
        "title": title,
        "body": content,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        print("Bark 推送状态：", response.status_code)

    except Exception as e:
        print("Bark 推送失败：", e)


def check_stock(name, sku):
    """检查京东商品库存"""

    url = "https://c0.3.cn/stock"

    params = {
        "skuId": sku,
        "area": AREA,
        "buyNum": 1,
        "ch": 1,
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.0 Mobile/15E148 Safari/604.1"
        )
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        print(f"\n{name} | SKU：{sku}")
        print("京东返回：", response.text)

        data = response.json()

        stock = data.get("stock", {})
        stock_state = stock.get("StockState")

        # 京东常见有货状态
        if stock_state == 33:

            print("🔥 发现有货！")

            bark_push(
                "🔥 京东有货提醒",
                f"{name} 有货了！\nSKU：{sku}"
            )

        else:

            print(
                f"暂时无货，库存状态：{stock_state}"
            )

    except Exception as e:

        print(
            f"检查 {name} 失败：{e}"
        )


# =========================
# 主程序
# =========================

if __name__ == "__main__":

    print("=" * 50)
    print("京东库存监控启动")
    print("监控商品数量：", len(PRODUCTS))
    print("开始时间：", datetime.now())
    print("=" * 50)

    for name, sku in PRODUCTS.items():

        check_stock(
            name,
            sku
        )

    print("=" * 50)
    print("本轮监控结束")
    print("=" * 50)
