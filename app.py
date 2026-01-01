import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd

st.set_page_config(layout="wide", page_title="Screener Saham AI")
st.title("📈 IHSG Stock Screener")

# Daftar Saham Populer
tickers = ["BBCA.JK", "BBRI.JK", "BMRI.JK", "TLKM.JK", "ASII.JK", "GOTO.JK", "ADRO.JK", "ANTM.JK", "AMMN.JK"]

def get_signal(symbol):
    try:
        df = yf.download(symbol, period="60d", interval="1d", progress=False)
        if df.empty: return None
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA20'] = ta.ema(df['Close'], length=20)
        last = df.iloc[-1]
        
        # Logika Sinyal
        if last['RSI'] < 30: 
            status = "WAJIB BUY"
        elif last['RSI'] > 70: 
            status = "WAJIB SELL"
        elif last['Close'] > last['EMA20']: 
            status = "HOLD"
        else: 
            status = "WAIT"
            
        return {
            "Emiten": symbol.replace(".JK", ""),
            "Harga": int(last['Close']),
            "RSI": round(last['RSI'], 1),
            "Rekomendasi": status
        }
    except: return None

if st.button('Mulai Scan Saham'):
    results = [get_signal(s) for s in tickers if get_signal(s) is not None]
    st.table(pd.DataFrame(results))
else:
    st.write("Klik tombol untuk melihat hasil analisis.")
