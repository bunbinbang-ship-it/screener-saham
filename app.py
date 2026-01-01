import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from textblob import TextBlob

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="StockIntel AI", layout="wide")

# CSS Sederhana Anti-Error
st.markdown('<style>.stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #eee; }</style>', unsafe_allow_html=True)

# --- 2. FUNGSI AMBIL DATA ---
@st.cache_data(ttl=600)
def get_data(symbol, period):
    # Mengambil data harga saja (paling stabil)
    df = yf.download(symbol, period=period, progress=False)
    return df

def analyze_sentiment(text):
    pol = TextBlob(text).sentiment.polarity
    if pol > 0.1: return "🟢 POSITIF", "#e6fffa"
    if pol < -0.1: return "🔴 NEGATIF", "#fff5f5"
    return "⚪ NETRAL", "#f8f9fa"

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("📈 StockIntel")
    ticker = st.text_input("Simbol (Contoh: BBCA.JK atau AAPL)", "BBCA.JK").upper()
    range_val = st.selectbox("Periode", ["3mo", "6mo", "1y", "2y"], index=2)
    st.caption("Gunakan .JK untuk saham Indonesia")

# --- 4. TAMPILAN UTAMA ---
if ticker:
    try:
        # 1. Ambil Data Harga
        df = get_data(ticker, range_val)
        
        if df.empty:
            st.error(f"Data tidak ditemukan untuk {ticker}. Pastikan penulisan benar.")
        else:
            st.header(f"Dashboard Saham: {ticker}")
            
            # Row 1: Metrics Sederhana dari Data Harga
            c1, c2, c3 = st.columns(3)
            last_price = float(df['Close'].iloc[-1])
            prev_price = float(df['Close'].iloc[-2])
            diff = last_price - prev_price
            pct = (diff / prev_price) * 100
            
            c1.metric("Harga Terakhir", f"{last_price:,.0f}", f"{pct:.2f}%")
            c2.metric("Tertinggi (Periode Ini)", f"{df['High'].max():,.0f}")
            c3.metric("Terendah (Periode Ini)", f"{df['Low'].min():,.0f}")

            # Row 2: Tabs
            t1, t2 = st.tabs(["📊 Grafik Teknikal", "📰 Berita & Sentimen"])
            
            with t1:
                # Grafik Candlestick
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'], name="Harga"
                )])
                # Tambah MA50
                ma50 = df['Close'].rolling(window=50).mean()
                fig.add_trace(go.Scatter(x=df.index, y=ma50, name="MA50", line=dict(color='orange')))
                fig.update_layout(xaxis_rangeslider_visible=False, height=500, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

            with t2:
                # Ambil berita tanpa membebani 'info'
                t_obj = yf.Ticker(ticker)
                news = t_obj.news
                if not news:
                    st.info("Tidak ada berita terbaru.")
                else:
                    for n in news[:5]:
                        lbl, color = analyze_sentiment(n['title'])
                        st.markdown(f"""
                        <div style="background-color:{color}; padding:10px; border-radius:5px; margin-bottom:10px; border: 1px solid #ddd;">
                            <small><b>{lbl}</b></small><br>
                            <a href="{n['link']}" target="_blank" style="text-decoration:none; color:black; font-weight:bold;">{n['title']}</a>
                        </div>
                        """, unsafe_allow_html=True)

    except Exception as e:
        st.error("Gagal memuat dashboard. Silakan coba segarkan halaman.")
                        
