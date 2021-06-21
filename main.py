import sys
import pyupbit
import time
import requests
import threading

def bull_market(ticker):
    try:
        df = pyupbit.get_ohlcv(ticker)
        ma5 = df['close'].rolling(window=5).mean()
        last_ma5 = ma5[-3]
        ma20 = df['close'].rolling(window=20).mean()
        last_ma20 = ma20[-3]

        df_hour = pyupbit.get_ohlcv(ticker, "minute60")
        ma5_hour = df_hour['close'].rolling(window=5).mean()
        last_ma5_hour = ma5_hour[-3]

        ma20_hour = df_hour['close'].rolling(window=20).mean()
        last_ma20_hour = ma20_hour[-3]

        price = pyupbit.get_current_price(ticker)


        if price > last_ma5 > last_ma20 and price > last_ma5_hour > last_ma20_hour:
            return True
        else:
            return False


    except:
        return None, None

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text}
                             )
    print(response)


myToken = "xoxb-2186286485602-2198982877889-hUFS54MwkG4c7aPBUS1Eq7g9"


tickers = pyupbit.get_tickers(fiat="KRW")

def printhello():
    for ticker in tickers:
        is_bull = bull_market(ticker)
        if is_bull:
            print(ticker, " 상승장",post_message(myToken, "#코인", "상승중" +ticker))

        else:
            print(ticker, " 하락장")


    # threading을 정의한다. 5초마다 반복 수행함.
    threading.Timer(1800, printhello).start()

printhello()


