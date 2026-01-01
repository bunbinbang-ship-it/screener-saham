import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from textblob import TextBlob

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="StockIntel - Dashboard Analisis Saham", layout="wide")

# Styling CSS untuk tampilan modern
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .news-card { padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }
    </style>
    """, unsafe_content_allowed=True)

# --- 2. FUNGSI HELPER ---
@st.cache_data
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

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🚀 StockIntel AI")
    st.subheader("Navigasi")
    ticker_input = st.text_input("Simbol Saham (Contoh: BBCA.JK atau AAPL)", "BBCA.JK").upper()
    time_period = st.selectbox("Periode Waktu", ["3mo", "6mo", "1y", "2y", "5y"], index=2)
    st.divider()
    st.info("Tips: Gunakan akhiran .JK untuk saham Indonesia.")

# --- 4. LOGIKA UTAMA ---
try:
    stock_obj, data = get_stock_data(ticker_input, time_period)
    info = stock_obj.info
    
    # Header Emiten
    st.title(f"{info.get('longName', ticker_input)}")
    st.caption(f"{info.get('sector', 'N/A')} | {info.get('industry', 'N/A')} | {info.get('exchange', 'N/A')}")

    # Row 1: Metrics Utama
    m1, m2, m3, m4 = st.columns(4)
    curr_price = data['Close'].iloc[-1]
    prev_price = data['Close'].iloc[-2]
    change = ((curr_price - prev_price) / prev_price) * 100

    m1.metric("Harga Terakhir", f"Rp {curr_price:,.0f}", f"{change:.2f}%")
    m2.metric("P/E Ratio", f"{info.get('trailingPE', 0):.2f}")
    m3.metric("PBV Ratio", f"{info.get('priceToBook', 0):.2f}")
    m4.metric("ROE", f"{info.get('returnOnEquity', 0)*100:.2f}%")

    # Row 2: Tabs Navigasi
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Teknikal", "📊 Fundamental", "🔍 Screener", "📰 Berita & Sentimen"])

    with tab1:
        st.subheader("Grafik Pergerakan Harga & MA")
        data['MA50'] = data['Close'].rolling(50).mean()
        data['MA200'] = data['Close'].rolling(200).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], 
                                   low=data['Low'], close=data['Close'], name="Harga"))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA50'], name="MA50 (Tren Pendek)", line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA200'], name="MA200 (Tren Panjang)", line=dict(color='red')))
        
        fig.update_layout(xaxis_rangeslider_visible=False, height=600, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Kinerja Keuangan")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Pendapatan Tahunan (Revenue)**")
            st.bar_chart(stock_obj.financials.loc['Total Revenue'])
        with c2:
            st.write("**Profil Perusahaan**")
            st.write(info.get('longBusinessSummary', 'Tidak ada deskripsi.'))

    with tab3:
        st.subheader("Quick Screener (Sektor Sejenis)")
        # Contoh sederhana screening saham sejenis (Watchlist)
        watchlist = ["BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "ASII.JK", "TLKM.JK"]
        if st.button("Scan Market"):
            results = []
            for t in watchlist:
                s_info = yf.Ticker(t).info
                results.append({
                    "Symbol": t,
                    "Price": s_info.get('currentPrice'),
                    "PE": s_info.get('trailingPE'),
                    "PBV": s_info.get('priceToBook')
                })
            st.table(pd.DataFrame(results))

    with tab4:
        st.subheader("Sentimen Berita Terkini")
        news_list = stock_obj.news
        if not news_list:
            st.warning("Berita tidak ditemukan.")
        else:
            for n in news_list[:8]:
                label, bg, border = get_sentiment(n['title'])
                st.markdown(f"""
                    <div class="news-card" style="background-color:{bg}; border-left-color:{border};">
                        <small>{label}</small>
                        <h4 style="margin:0;"><a href="{n['link']}" target="_blank" style="text-decoration:none; color:#1f1f1f;">{n['title']}</a></h4>
                        <small style="color:#666;">{n['publisher']} | {datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b %Y')}</small>
                    </div>
                """, unsafe_content_allowed=True)

except Exception as e:
    st.error(f"Terjadi kesalahan: Pastikan simbol ticker benar atau koneksi internet stabil.")

