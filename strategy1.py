import flet as ft
import numpy as np
import time
from datetime import datetime

class MyContainer(ft.UserControl):
    global t,bb_dev,bb_window
        
   
    t = ft.Text()
    bb_window=ft.Text()
    bb_dev=ft.Text()
    def build(self):
        def slider_changed_rsi(e):
            print(e.control.value)
            t.value =e.control.value
            print(e.control.value)
        def slider_changed_bb_window(e):
            print(e.control.value)
            bb_window.value = e.control.value
        def slider_changed_bb_dev(e):
            print(e.control.value)
            bb_dev.value =e.control.value
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "RSI Indicator",
                        size=13,
                        font_family="Platypi",
                        weight=ft.FontWeight.W_900,
                        text_align=ft.TextAlign.CENTER,
                        color="#000000"
                    ),
                    ft.Slider(min=7,value=14, max=70, divisions=63, label="{value}", on_change=slider_changed_rsi,thumb_color="#d9113a",active_color="#d9113a",inactive_color="#d9113a"),
                    ft.Text(
                        "Bollinger Band",
                        size=13,
                        font_family="Platypi",
                        weight=ft.FontWeight.W_900,
                        text_align=ft.TextAlign.CENTER,
                        color="#000000"
                    ),
                    ft.TextField(label="Period",value=12,height=50,color=ft.colors.BLACK,border_color="#d9113a",on_change=slider_changed_bb_window),
                    ft.Text(
                        "Deviation",
                        size=13,
                        font_family="Platypi",
                        weight=ft.FontWeight.W_900,
                        text_align=ft.TextAlign.CENTER,
                        color="#000000"
                    ),
                    ft.Slider(min=1,max=10,divisions=10,value=2,label="{value}", on_change=slider_changed_bb_window,thumb_color="#d9113a",active_color="#d9113a",inactive_color="#d9113a"),
                    ft.Text(
                        "Candle Time",
                        size=13,
                        font_family="Platypi",
                        weight=ft.FontWeight.W_900,
                        text_align=ft.TextAlign.CENTER,
                        color="#000000"
                    ),
                    ft.Slider(value=60,min=5,max=300,divisions=60,label="{value}", on_change=slider_changed_bb_dev,thumb_color="#d9113a",active_color="#d9113a",inactive_color="#d9113a"),
                ]
            ),
            padding=20,
            bgcolor="#fecf00",
            border_radius=ft.border_radius.all(10),
        )
    def get_rsi_slider_value(e):
        return t.value

    def get_bollinger_band_period_value(e):
        return bb_window.value
    def get_bollinger_band_dev_value(e):
        return bb_dev.value
    
def get_trading_session(timestamp):
    # Define the trading session time ranges
    london_session_start = datetime.strptime("08:00", "%H:%M").time()
    london_session_end = datetime.strptime("16:00", "%H:%M").time()
    
    new_york_session_start = datetime.strptime("13:00", "%H:%M").time()
    new_york_session_end = datetime.strptime("21:00", "%H:%M").time()
    
    asian_session_start = datetime.strptime("00:00", "%H:%M").time()
    asian_session_end = datetime.strptime("08:00", "%H:%M").time()
    
    # Convert the timestamp to a datetime object
    timestamp_datetime = datetime.fromtimestamp(timestamp // 1000000000)
    time = timestamp_datetime.time()
    
    # Determine the trading session based on the timestamp
    if london_session_start <= time <= london_session_end:
        return "London Trading Session"
    elif new_york_session_start <= time <= new_york_session_end:
        return "New York Trading Session"
    elif asian_session_start <= time <= asian_session_end:
        return "Asian Trading Session"
    else:
        return "Outside of Trading Session"
def calculate_rsi(data, period=13):
    closes = np.array([candle['close'] for candle in data])
    changes = np.diff(closes)
    ups = changes[changes >= 0]
    downs = -changes[changes < 0]

    avg_gain = np.mean(ups[:period])
    avg_loss = np.mean(downs[:period])

    rs = avg_gain / avg_loss if avg_loss != 0 else np.inf
    rsi = 100 - (100 / (1 + rs))

    for i in range(period, len(data)):
        delta = closes[i] - closes[i - 1]
        gain = delta if delta > 0 else 0
        loss = -delta if delta < 0 else 0

        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period

        rs = avg_gain / avg_loss if avg_loss != 0 else np.inf
        rsi = np.append(rsi, 100 - (100 / (1 + rs)))

    return rsi

def calculate_bollinger_bands(data, window, num_std_dev):
    closes = np.array([candle['close'] for candle in data])
    sma = np.convolve(closes, np.ones(window)/window, mode='valid')
    std_dev = np.std(closes[:window] - sma[0])  # Calculate std dev for the initial window

    upper_band = sma + num_std_dev * std_dev
    lower_band = sma - num_std_dev * std_dev

    for i in range(len(closes) - window):
        std_dev = np.std(closes[i:i+window] - sma[i])
        upper_band = np.append(upper_band, sma[i] + num_std_dev * std_dev)
        lower_band = np.append(lower_band, sma[i] - num_std_dev * std_dev)

    return upper_band, lower_band

def trade_strategy(trade_triger,trade_amount,trade_time,switch_signal):
    global keep_running
    
    container=MyContainer()
    period_rsi=container.get_rsi_slider_value()
    window=container.get_bollinger_band_period_value()
    dev=container.get_bollinger_band_dev_value()
    goal=["EURUSD","EURJPY","GBPJPY","AUDUSD","GBPUSD","AUDJPY","AUDCAD","USDCHF","USDCAD","EURGBP"]
        
    for i in range(len(goal)):
        data=trade_triger.get_candles(goal[i],60,200,time.time())
        print("running......")
        rsi=calculate_rsi(data,14)
        bollingerband=calculate_bollinger_bands(data, 12,2)
        if data[-1]['close'] > bollingerband[0][-1] and rsi[-1]>= 50:
            if switch_signal:
                check,id=trade_triger.buy(trade_amount,goal[i],"put",trade_time)
                return goal[i],"put",id
            else:
                return goal[i],"put"
            
        elif data[-1]['close'] < bollingerband[1][-1] and rsi[-1] <= 50:
            if switch_signal:
                check,id=trade_triger.buy(trade_amount,goal[i],"call",trade_time)
                return goal[i],"call",id
            else:
                return goal[i],"call"


status="none"
def print_trades(data, upper_band, lower_band):
    Total_win=0
    Total_lose=0
    new_york_session=0
    london_session=0
    asian_session=0
    win_2=0
    loss_2=0
    win_1=0
    loss_1=0
    closes = np.array([candle['close'] for candle in data])
    rsi_values = calculate_rsi(data)
    print(data)
    initmoney=5
    for i in range(len(closes) -13):
        if closes[i] > upper_band[i-1] and rsi_values[i-1] >= 65:
            if closes[i+4]<closes[i]:
                Total_win=Total_win+1
                if get_trading_session(data[i]['at'])=="New York Trading Session":
                    new_york_session=new_york_session+1
                if get_trading_session(data[i]['at'])=="London Trading Session":
                    london_session=london_session+1
                if get_trading_session(data[i]['at'])=="Asian Trading Session":
                    asian_session=asian_session+1
            else:
                Total_lose=Total_lose+1
            if closes[i+2]<closes[i]:
                win_2=win_2+1
            else:
                loss_2=loss_2+1
            if closes[i+1]<closes[i]:
                win_1=win_1+1
            else:
                loss_1=loss_1+1
            print("Sell - Date:", data[i]['at'], "Close:", closes[i], "RSI:", rsi_values[i-1], "Close:", closes[i+4],status)
        elif closes[i] < lower_band[i-1] and rsi_values[i-1] <= 35:
            if closes[i+4]>closes[i]:
                Total_win=Total_win+1
                if get_trading_session(data[i]['at'])=="New York Trading Session":
                    new_york_session=new_york_session+1
                if get_trading_session(data[i]['at'])=="London Trading Session":
                    london_session=london_session+1
                if get_trading_session(data[i]['at'])=="Asian Trading Session":
                    asian_session=asian_session+1
            else:
                Total_lose=Total_lose+1
            if closes[i+2]>closes[i]:
                win_2=win_2+1
            else:
                loss_2=loss_2+1
            if closes[i+1]>closes[i]:
                win_1=win_1+1
            else:
                loss_1=loss_1+1
            print("Sell - Date:", data[i]['at'], "Close:", closes[i], "RSI:", rsi_values[i-1],"Close:", closes[i+4],status)
    return Total_win,Total_lose,london_session,new_york_session,asian_session,win_1,win_2,loss_1,loss_2
def trade_strategy_logic(trade_triger):
    # Example usage:
    Total_win=0
    Total_lose=0
    new_york_session=0
    london_session=0
    asian_session=0
    win_2=0
    loss_2=0
    win_1=0
    loss_1=0
    goal=["EURUSD","EURJPY","GBPJPY","AUDUSD","GBPUSD","AUDJPY","AUDCAD","USDCHF","USDCAD","EURGBP"]
    for k in range(len(goal)):
        end_from_time=time.time()
        ANS=[]
        for i in range(20):
            data=trade_triger.get_candles(goal[k], 60, 1000, end_from_time)
            ANS =data+ANS
            end_from_time=int(data[0]["from"])-1
        candle_data =ANS
        upper_band, lower_band = calculate_bollinger_bands(candle_data,12,2)
        print(len(ANS))
        result=print_trades(candle_data, upper_band, lower_band)
        Total_win=Total_win+result[0]
        Total_lose=Total_lose+result[1]
        new_york_session=new_york_session+result[2]
        london_session=london_session+result[3]
        asian_session=asian_session+result[4]
        win_2=win_2+result[5]
        loss_2=loss_2+result[6]
        win_1=win_1+result[7]
        loss_1=loss_1+result[8]
        print(str(goal[k])+"batch done")
    
    return Total_win,Total_lose,new_york_session,london_session,asian_session,win_2,win_1

