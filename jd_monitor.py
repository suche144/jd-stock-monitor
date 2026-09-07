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
        "skuNum": f"{sk
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
