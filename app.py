import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from textblob import TextBlob

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="StockIntel - Dashboard Saham", layout="wide")

# CSS satu baris agar tidak IndentationError
st.markdown('<style>.main { background-color: #f8f9fa; } .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); } .news-card { padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>', unsafe_allow_html=True)

# --- 2. FUNGSI HELPER ---
@st.cache_data(ttl=3600) # Cache selama 1 jam
def get_stock_data(symbol, p):
    ticker_obj = yf.Ticker(symbol)
    df = ticker_obj.history(period=p)
    return ticker_obj, df

def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.1:
        return "🟢 POSITIF", "#e6fffa", "green"
    elif analysis.sentiment.polarity < -0.1:
        return "🔴 NEGATIF", "#fff5f5", "red"
    else:
        return "⚪ NETRAL", "#f8f9fa", "gray"

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🚀 StockIntel AI")
    ticker_input = st.text_input("Ketik Simbol (Contoh: BBCA.JK atau AAPL)", "BBCA.JK").upper()
    time_period = st.selectbox("Periode", ["3mo", "6mo", "1y", "2y", "5y"], index=2)
    st.info("PENTING: Gunakan akhiran .JK untuk saham Indonesia.")

# --- 4. LOGIKA UTAMA ---
if ticker_input:
    try:
        stock_obj, data = get_stock_data(ticker_input, time_period)
        
        if data.empty:
            st.warning(f"Data untuk {ticker_input} tidak ditemukan. Coba cek penulisan simbol.")
        else:
            info = stock_obj.info
            
            # Header
            st.title(f"{info.get('longName', ticker_input)}")
            
            # Row 1: Metrics (Gunakan .get() dengan default 0 agar tidak error)
            m1, m2, m3, m4 = st.columns(4)
            curr_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2]
            change = ((curr_price - prev_price) / prev_price) * 100

            m1.metric("Harga Terakhir", f"Rp {curr_price:,.0f}", f"{change:.2f}%")
            m2.metric("P/E Ratio", f"{info.get('trailingPE', 0):.2f}")
            m3.metric("PBV Ratio", f"{info.get('priceToBook', 0):.2f}")
            m4.metric("ROE", f"{info.get('returnOnEquity', 0)*100:.2f}%")

            # Row 2: Tabs
            tab1, tab2, tab3 = st.tabs(["📈 Teknikal", "📊 Fundamental", "📰 Berita"])

            with tab1:
                data['MA50'] = data['Close'].rolling(50).mean()
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="Harga"))
                fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name="MA50", line=dict(color='orange')))
                fig.update_layout(xaxis_rangeslider_visible=False, height=500)
                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.write(f"**Profil:** {info.get('longBusinessSummary', 'Deskripsi tidak tersedia.')}")
                if 'Total Revenue' in stock_obj.financials.index:
                    st.bar_chart(stock_obj.financials.loc['Total Revenue'])

            with tab3:
                news_list = stock_obj.news
                for n in news_list[:5]:
                    label, bg, border = get_sentiment(n['title'])
                    st.markdown(f'<div class="news-card" style="background-color:{bg}; border-left-color:{border};"><small>{label}</small><br><a href="{n["link"]}">{n["title"]}</a></div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Terjadi masalah teknis: {e}")
    
