import os
import re===========
# 需要监控的商品
# =================

PRODUCTS = {
    "花朵系列": "10217041125002",
    "水果系列": "10196364421727",
    "花的礼物": "1023433061095610",
}

# 深圳
AREA = os.getenv("JD_AREA", "19_1607_0_0")

# Bark
BARK_KEY = os.getenv("BARK_KEY")


def bark_push(name, sku, stock):
    if not BARK_KEY:
        print("BARK_KEY 尚未配置")
        return

    url = f"https://api.day.app/{BARK_KEY}"

    data = {
        "title": "🔥 京东库存提醒",
        "body": f"{name}\n库存状态：{stock}\nSKU：{sku}",
        "url": f"https://item.jd.com/{sku}.html",
    }

    try:
        r = requests.post(url, json=data, timeout=10)
        print("Bark:", r.status_code)
    except Exception as e:
        print("Bark 推送失败:", e)


def check_stock(name, sku):

    # 京东库存接口
    url = "https://fts.jd.com/areaStockState/mget"

    params = {
        "app": "cart_pc",
        "ch": "1",
        "skuNum": f"{sku},1",
        "area": AREA.replace("_", ","),
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.0 Mobile/15E148 Safari/604.1"
        ),
        "Referer": "https://cart.jd.com/",
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        print(f"\n{name} | SKU：{sku}")
        print("HTTP状态：", response.status_code)
        print("返回：", response.text)

        response.raise_for_status()

        data = response.json()

        # 京东接口通常返回：
        # {"SKU":{"a":"33","b":"1","c":"5"}}

        item = data.get(str(sku))

        if not item:
            print("没有找到商品库存信息")
            return

        state = str(item.get("a", ""))
        quantity = item.get("c", "")

        # 33 = 有货
        if state == "33":

            print("🔥 有货！")

            bark_push(
                name,
                sku,
                f"有货，库存：{quantity}"
            )

        elif state == "34":

            print("❌ 无货")

        else:

            print(
                f"库存状态：{state}，数量：{quantity}"
            )

    except Exception as e:

        print(
            f"检查 {name} 失败：{e}"
        )


if __name__ == "__main__":

    print("=" * 50)
    print("京东库存监控启动")
    print("时间：", datetime.now())
    print("监控商品：", len(PRODUCTS))
    print("地区：深圳")
    print("=" * 50)

    for name, sku in PRODUCTS.items():

        check_stock(
            name,
            sku
        )

    print("=" * 50)
    print("本轮监控结束")
    print("=" * 50)
