import ccxt
import time
import telebot

# --- 配置区 ---
TOKEN = '8533316652:AAGN1Z7KuUmyOx3DhYXJ9F5drmWVDIRqxbs'
CHAT_ID = '5737626910'
SYMBOLS = ['BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT', 'PEPE/USDT:USDT']
CHECK_INTERVAL = 300 

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.okx()

def get_market_data(symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        funding = exchange.fetch_funding_rate(symbol)
        inst_id = symbol.replace('/', '-').replace(':USDT', '-SWAP')
        oi_data = exchange.public_get_public_open_interest(params={'instId': inst_id})
        oi_val = float(oi_data['data'][0]['oi'])
        
        score = 50 
        rate = funding['fundingRate'] * 100
        if rate < -0.01: score += 20 
        
        return {
            'price': ticker['last'],
            'score': score,
            'oi': oi_val,
            'rate': f"{rate:.4f}%"
        }
    except Exception as e:
        return None

def main():
    print("🤖 监控机器人已启动...")
    # 这里会测试你的新 Token 是否有效
    bot.send_message(CHAT_ID, "✅ 监控系统已成功迁移至新 Token，运行正常！")
    
    while True:
        for s in SYMBOLS:
            data = get_market_data(s)
            if data and data['score'] >= 50:
                msg = (
                    f"🔥 **行情异动**\n"
                    f"🏷️ **币种**: `{s.split('/')[0]}`\n"
                    f"💰 **价格**: `{data['price']}`\n"
                    f"📊 **策略分**: `{data['score']}`\n"
                    f"⚓ **费率**: `{data['rate']}`"
                )
                bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
