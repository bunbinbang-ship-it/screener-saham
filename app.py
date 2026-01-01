import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(layout="wide", page_title="IHSG Pro Dashboard")

# CSS untuk mempercantik tampilan (Dark Mode Premium)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #58a6ff; }
    table { border-radius: 10px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 IHSG Smart Dashboard")
st.write("Sinyal Real-Time berdasarkan Analisis Algoritma")

# Pilihan Saham
tickers = ["BBCA.JK", "BBRI.JK", "BMRI.JK", "TLKM.JK", "ASII.JK", "GOTO.JK", "ADRO.JK", "ANTM.JK", "AMMN.JK"]

def get_data(symbol):
    try:
        df = yf.download(symbol, period="60d", interval="1d", progress=False)
        if df.empty: return None
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA20'] = ta.ema(df['Close'], length=20)
        last = df.iloc[-1]
        
        # Logika Warna & Sinyal
        rsi_val = last['RSI']
        price = last['Close']
        ema = last['EMA20']
        
        if rsi_val < 35: signal = "🟢 BUY NOW"
        elif rsi_val > 65: signal = "🔴 SELL NOW"
        elif price > ema: signal = "🟡 HOLD"
        else: signal = "⚪ WAIT"
            
        return {
            "Emiten": symbol.replace(".JK", ""),
            "Harga": f"Rp {int(price):,}",
            "RSI (14)": round(rsi_val, 1),
            "Rekomendasi": signal
        }
    except: return None

# Tampilan Menu Utama
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Menu")
    btn = st.button('🔄 Update Analisis')

with col2:
    if btn:
        with st.spinner('Menganalisis Bursa...'):
            results = []
            for s in tickers:
                res = get_data(s)
                if res: results.append(res)
            
            if results:
                st.subheader("Hasil Screening Terkini")
                st.table(pd.DataFrame(results))
            else:
                st.error("Gagal menarik data. Coba lagi.")
    else:
        st.info("Tekan tombol 'Update Analisis' di samping untuk memulai.")
