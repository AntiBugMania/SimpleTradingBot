import json
import time
from ib_insync import *
import pandas as pd

# ---- LOAD CONFIG ----
with open('config/consolidation_breakout.json', 'r') as f:
    cfg = json.load(f)

symbol = cfg['symbol']
exchange = cfg['exchange']
currency = cfg['currency']
order_size = cfg['order_size']
breakout_length = cfg['breakout_length']

# ---- CONNECT TO IBKR ----
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# ---- REQUEST HISTORICAL DATA ----
contract = Stock(symbol, exchange, currency)

print("Bot started. Checking every 5 minutes... (CTRL+C to stop)")

try:
    while True:
        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr= '2 D',
            barSizeSetting= '5 mins',
            whatToShow='TRADES',
            useRTH=True
        )

        df = util.df(bars)

        if len(df) > breakout_length:
            recent_high = df['close'][-breakout_length-1:-1].max()
            current_close = df['close'].iloc[-1]

            if current_close > recent_high:
                print(f"[{pd.Timestamp.now()}] Breakout detected! Would BUY {order_size} {symbol} here.")
                # Optionally check you have no existing position before buying!
                order = MarketOrder('BUY', order_size)
                trade = ib.placeOrder(contract, order)
                ib.sleep(1)
                print(trade)
            else:
                print(f"[{pd.Timestamp.now()}] No breakout. No trade.")
        else:
            print(f"[{pd.Timestamp.now()}] Not enough data to calculate breakout.")

        # Sleep for 5 minutes, then check again
        time.sleep(5 * 60)

except KeyboardInterrupt:
    print("Botstopped by user.")

finally:
    ib.disconnect()