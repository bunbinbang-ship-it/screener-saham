import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# Konfigurasi Tampilan
st.set_page_config(layout="wide", page_title="SAHAM KU")

# CSS untuk desain teks 90px dan Menu Bawah (Sticky Navigation)
st.markdown("""
    <style>
    /* Judul Besar */
    .judul-utama {
        font-size: 90px;
        font-weight: bold;
        text-align: center;
        margin-top: 15vh;
        color: #58a6ff;
    }
    
    /* Menu Navigasi Bawah */
    .footer-menu {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #161b22;
        color: white;
        text-align: center;
        padding: 10px 0;
        display: flex;
        justify-content: space-around;
        border-top: 1px solid #30363d;
        z-index: 999;
    }
    
    .menu-item {
        font-size: 12px;
        cursor: pointer;
    }
    
    /* Ruang kosong agar konten tidak tertutup menu */
    .spacer { margin-bottom: 100px; }
    </style>
    """, unsafe_allow_html=True)

# --- TAMPILAN DEPAN ---
st.markdown('<div class="judul-utama">SAHAM KU</div>', unsafe_allow_html=True)

# Tombol Scan Utama di Tengah
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button('🚀 Mulai Analisis Saham'):
        st.write("Sedang memproses data...")
        # (Logika analisis Anda di sini)

# Memberi ruang di bawah agar tidak tertutup menu
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# --- MENU NAVIGASI BAWAH (Simulasi Visual) ---
st.markdown("""
    <div class="footer-menu">
        <div class="menu-item">☰<br>Menu</div>
        <div class="menu-item">🏠<br>Home</div>
        <div class="menu-item">🔍<br>Cari</div>
        <div class="menu-item">⭐<br>Watchlist</div>
        <div class="menu-item">📖<br>Jurnal</div>
        <div class="menu-item">👤<br>Google Login</div>
    </div>
    """, unsafe_allow_html=True)      
    
