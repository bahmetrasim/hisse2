import streamlit as st
import yfinance as yf
import pandas as pd
import time
import random
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime

st.set_page_config(page_title="Anayasa Tarayıcı v8", layout="centered")
st.title("Yatırım Anayasası v8")
st.markdown("Güvenli mod: Kontrollü tarama aktif.")

liste = ["AAPL", "MSFT", "SOFI", "PLTR", "RIVN", "F", "INTC", "CHWY", "U", "LCID", "T", "PFE", "AMD", "META", "TSLA"]

if st.button("Taramayı Başlat"):
    uygunlar = []
    basarili_tarama = 0
    son_tarih = None
    
    bar = st.progress(0)
    for i, ticker in enumerate(liste):
        bar.progress(int((i+1)/len(liste)*100))
        try:
            time.sleep(random.uniform(1.5, 2.5)) 
            df = yf.download(ticker, period="2mo", interval="1d", progress=False, 
                             threads=False, user_agent='Mozilla/5.0')
            
            if len(df) < 25: continue
            
            basarili_tarama += 1
            son_tarih = df.index[-1].strftime('%d %B %Y') # Fiyatın ait olduğu gün
            
            close = df['Close'].squeeze()
            ema9 = close.ewm(span=9, adjust=False).mean()
            ema21 = close.ewm(span=21, adjust=False).mean()
            
            if (float(close.iloc[-1]) <= 50) and \
               (float(ema9.iloc[-2]) <= float(ema21.iloc[-2])) and \
               (float(ema9.iloc[-1]) > float(ema21.iloc[-1])):
                
                uygunlar.append({"Sembol": ticker, "Fiyat": round(float(close.iloc[-1]), 2)})
        except: continue
        
    st.divider()
    # Reel raporlama
    st.write(f"📊 **Tarama Raporu:**")
    st.write(f"- Toplam taranan hisse sayısı: {len(liste)}")
    st.write(f"- Reel veri çekilen hisse sayısı: {basarili_tarama}")
    st.write(f"- Baz alınan fiyat tarihi: **{son_tarih}**")
    
    if uygunlar: st.dataframe(pd.DataFrame(uygunlar))
    else: st.warning("Bu listede Anayasa'ya uygun hisse yok. Sabır disiplindir.")
