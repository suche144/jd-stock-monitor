import os
import 

    url = f"https://api.day.app/{BARK_KEY}"

    daurl, json=data, timeout=10)
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
        quantity = item.get("c", ""_main__":

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
