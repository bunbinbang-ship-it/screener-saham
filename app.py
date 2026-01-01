import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# Konfigurasi Dasar
st.set_page_config(layout="wide", page_title="SAHAMKU")

# CSS untuk desain satu baris dan Menu Bawah
st.markdown("""
    <style>
    /* Membuat tulisan SAHAMKU satu baris */
    .judul-sahamku {
        font-size: clamp(40px, 10vw, 80px); /* Ukuran fleksibel agar tetap satu baris */
        font-weight: bold;
        text-align: center;
        color: #58a6ff;
        margin-top: 50px;
        white-space: nowrap;
    }
    
    /* Navigasi Bawah yang tetap di tempat (Sticky) */
    .stBottomBlock {
        position: fixed;
        bottom: 0;
        background: #161b22;
        padding: 10px;
        z-index: 100;
    }
    
    /* Sembunyikan footer bawaan streamlit agar bersih */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="judul-sahamku">SAHAMKU</div>', unsafe_allow_html=True)
st.write("<p style='text-align: center; color: gray;'>Smart Analysis & Portfolio</p>", unsafe_allow_html=True)

# --- FUNGSI ANALISIS CEPAT ---
def get_fast_data(symbol):
    try:
        # Mengambil hanya 40 hari agar super cepat
        df = yf.download(symbol, period="40d", interval="1d", progress=False, threads=False)
        if df.empty: return None
        
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA20'] = ta.ema(df['Close'], length=20)
        
        last = df.iloc[-1]
        price = float(last['Close'])
        rsi_val = float(last['RSI'])
        ema_val = float(last['EMA20'])
        
        if rsi_val < 35: signal = "🟢 BUY"
        elif rsi_val > 65: signal = "🔴 SELL"
        elif price > ema_val: signal = "🟡 HOLD"
        else: signal = "⚪ WAIT"
            
        return {
            "Emiten": symbol.replace(".JK", ""),
            "Harga": f"Rp {int(price):,}",
            "RSI": round(rsi_val, 1),
            "Sinyal": signal
        }
    except: return None

# --- TOMBOL ANALISIS ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button('🚀 JALANKAN SCAN CEPAT', use_container_width=True):
    with st.spinner('Mengambil data bursa...'):
        watchlist = ["BBCA.JK", "BBRI.JK", "BMRI.JK", "TLKM.JK", "ASII.JK", "GOTO.JK", "ADRO.JK", "ANTM.JK"]
        results = [get_fast_data(s) for s in watchlist]
        results = [r for r in results if r is not None]
        
        if results:
            st.table(pd.DataFrame(results))
        else:
            st.error("Gagal mengambil data. Coba lagi nanti.")

# --- MENU NAVIGASI BAWAH (BISA DIKLIK) ---
st.markdown("<br><br><br>", unsafe_allow_html=True) # Ruang agar tidak tertutup menu
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    if st.button("☰\nMenu"): st.toast("Menu dibuka")
with m2:
    if st.button("🏠\nHome"): st.rerun()
with m3:
    if st.button("🔍\nCari"): st.toast("Fitur Cari segera hadir")
with m4:
    if st.button("⭐\nWatch"): st.toast("Membuka Watchlist")
with m5:
    if st.button("👤\nLogin"): st.toast("Menghubungkan ke Google...")
