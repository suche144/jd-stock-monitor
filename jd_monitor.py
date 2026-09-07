import os
import re
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

BARK_KEY = os.getenv("BARK_KEY")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def bark_push(name, sku):
    if not BARK_KEY:
        print("⚠️ BARK_KEY 尚未配置")
        return

    url = f"https://api.day.app/{BARK_KEY}"

    data = {
        "title": "🔥 京东有货提醒",
        "body": f"{name}\n检测到可能有货！\nSKU：{sku}",
        "url": f"https://item.jd.com/{sku}.html",
    }

    try:
        r = requests.get(url, params=data, timeout=10)
        print("Bark 推送：", r.status_code)
    except Exception as e:
        print("Bark 推送失败：", e)


def check_stock(name, sku):
    url = f"https://item.jd.com/{sku}.html"

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
            allow_redirects=True,
        )

        print(f"\n{name} | SKU：{sku}")
        print("HTTP：", r.status_code)
        print("最终地址：", r.url)

        text = r.text

        if not text:
            print("❌ 页面为空")
            return

        # 判断是否被京东拦截
        if "访问受限" in text or "安全验证" in text or "验证码" in text:
            print("⚠️ 京东触发了安全验证")
            return

        # 常见无货关键词
        out_words = [
            "无货",
            "暂时无货",
            "库存不足",
            "已售罄",
            "补货中",
        ]

        # 常见有货关键词
        in_words = [
            "有货",
            "现货",
            "立即购买",
            "加入购物车",
        ]

        out_found = [x for x in out_words if x in text]
        in_found = [x for x in in_words if x in text]

        print("有货关键词：", in_found)
        print("无货关键词：", out_found)

        if in_found and not out_found:
            print("🔥🔥🔥 可能有货！")
            bark_push(name, sku)

        elif out_found:
            print("❌ 可能无货")

        else:
            print("⚠️ 无法确定库存状态")

    except Exception as e:
        print("❌ 请求失败：", e)


if __name__ == "__main__":
    print("=" * 60)
    print("京东商品页面库存监控")
    print("时间：", datetime.now())
    print("监控商品：", len(PRODUCTS))
    print("=" * 60)

    for name, sku in PRODUCTS.items():
        check_stock(name, sku)

    print("=" * 60)
    print("本轮监控结束")
    print("=" * 60)
