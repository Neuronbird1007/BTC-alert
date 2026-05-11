import requests
import os

# 从 GitHub Secrets 读取你的电报密码
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHAT_ID = os.environ.get("TG_CHAT_ID")

def send_telegram(message):
    """发送 TG 消息的函数"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("发送TG失败:", e)

def check_weekly_sma20():
    try:
        # 直接拉取币安公开接口（不需要任何账号），获取最近21周的BTC周线数据
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1w&limit=21"
        data = requests.get(url).json()
        
        # data[-2] 是上周（刚刚在周一早8点收盘定型的那根周线）
        last_week_close = float(data[-2][4])
        
        # 计算过去20周的简单均线 (SMA 20)
        close_prices = [float(candle[4]) for candle in data[-21:-1]]
        sma_20 = sum(close_prices) / 20
        
        print(f"上周收盘价: {last_week_close} | 20周均线: {sma_20}")
        
        # 核心右侧判决逻辑
        if last_week_close < sma_20:
            msg = f"🚨 <b>【做空扳机触发！牛市危急】</b>\n\nBTC 周线已无情跌破 20周均线！\n上周收盘价: <b>${last_week_close:.2f}</b>\n20周均线值: <b>${sma_20:.2f}</b>\n\n⚠️ 请立刻核查 ETF 流出情况，准备清仓现货，执行右侧做空纪律！"
            send_telegram(msg)
        else:
            print("均线未破，安全，不需要打扰。")
            
    except Exception as e:
        print("运行出错:", e)

if __name__ == "__main__":
    check_weekly_sma20()
