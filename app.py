import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go

# 1. Konfigurasi Layout Website (Lebar & Dark Mode)
st.set_page_config(layout="wide", page_title="Dashboard Pro IHSG")

# 2. Styling CSS untuk tampilan Website Premium
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .main-header { font-size: 36px; font-weight: bold; color: #58a6ff; text-align: center; margin-bottom: 20px; }
    div[data-testid="stMetric"] { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">📈 Terminal Saham IHSG Pro</div>', unsafe_allow_html=True)

# 3. Sidebar untuk Pengaturan
st.sidebar.header("Konfigurasi Web")
selected_tickers = st.sidebar.multiselect(
    "Pilih Daftar Pantau (Watchlist):",
    ["BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "TLKM.JK", "ASII.JK", "GOTO.JK", "ADRO.JK", "ANTM.JK", "AMMN.JK"],
    default=["BBCA.JK", "BBRI.JK", "BMRI.JK", "TLKM.JK"]
)

# 4. Fungsi Analisis
def analyze_stock(symbol):
    try:
        df = yf.download(symbol, period="100d", interval="1d", progress=False, threads=False)
        if df.empty: return None
        
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA20'] = ta.ema(df['Close'], length=20)
        
        last = df.iloc[-1]
        close_price = float(last['Close'])
        rsi_val = float(last['RSI'])
        ema_val = float(last['EMA20'])
        
        # Logika Sinyal
        if rsi_val < 35: 
            rec = "🟢 STRONG BUY"
        elif rsi_val > 65: 
            rec = "🔴 STRONG SELL"
        elif close_price > ema_val: 
            rec = "🟡 HOLD (UPTREND)"
        else: 
            rec = "⚪ WAIT & SEE"
            
        return {
            "Emiten": symbol.replace(".JK", ""),
            "Harga Terakhir": f"Rp {close_price:,.0f}",
            "RSI (14)": round(rsi_val, 2),
            "Rekomendasi": rec,
            "Raw_Price": close_price,
            "DF": df
        }
    except: return None

# 5. Tampilan Website Utama (Tabs)
tab1, tab2 = st.tabs(["📊 Screener Utama", "📈 Analisis Grafik"])

with tab1:
    if st.button('🚀 Jalankan Analisis Website'):
        results = []
        # Menggunakan kolom (Columns) untuk ringkasan metric di atas
        m_col1, m_col2, m_col3 = st.columns(3)
        
        for s in selected_tickers:
            data = analyze_stock(s)
            if data: results.append(data)
        
        if results:
            df_final = pd.DataFrame(results).drop(columns=['DF', 'Raw_Price'])
            st.table(df_final)
            
            m_col1.metric("Total Scan", f"{len(results)} Emiten")
            m_col2.metric("Market", "IHSG (Jakarta)", "Open")
            m_col3.metric("Status Server", "Online", "Stable")
        else:
            st.warning("Gagal mengambil data. Pastikan file requirements.txt sudah benar.")

with tab2:
    st.subheader("Visualisasi Grafik Teknikal")
    stock_to_view = st.selectbox("Pilih saham untuk melihat grafik:", selected_tickers)
    
    view_data = analyze_stock(stock_to_view)
    if view_data:
        df_chart = view_data['DF']
        fig = go.Figure(data=[go.Candlestick(x=df_chart.index,
                        open=df_chart['Open'], high=df_chart['High'],
                        low=df_chart['Low'], close=df_chart['Close'])])
        fig.update_layout(template="plotly_dark", title=f"Pergerakan Harga {stock_to_view}")
        st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.write("Web ini berjalan otomatis menggunakan data Yahoo Finance.")
