import streamlit as st
import yfinance as yf
import pandas as pd
import time
import random
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Anayasa Tarayıcı v7", layout="centered")
st.title("Yatırım Anayasası v7")
st.markdown("Yahoo Engeli Aşıldı. Yavaş ve kontrollü tarama modu aktif.")

# Manuel liste (Daha güvenli, engellenmez)
liste = ["AAPL", "MSFT", "SOFI", "PLTR", "RIVN", "F", "INTC", "CHWY", "U", "LCID", "T", "PFE", "AMD", "META", "TSLA"]

if st.button("Taramayı Başlat"):
    uygunlar = []
    bar = st.progress(0)
    
    for i, ticker in enumerate(liste):
        bar.progress(int((i+1)/len(liste)*100))
        try:
            # "İnsan gibi" davran: Rastgele bekleme
            time.sleep(random.uniform(1.5, 3.0)) 
            
            # User-Agent maskeleme ile çekim
            df = yf.download(ticker, period="2mo", interval="1d", progress=False, 
                             threads=False, user_agent='Mozilla/5.0')
            
            if len(df) < 25: continue
            
            close = df['Close'].squeeze()
            ema9 = close.ewm(span=9, adjust=False).mean()
            ema21 = close.ewm(span=21, adjust=False).mean()
            
            # KONTROL
            if (float(close.iloc[-1]) <= 50) and \
               (float(ema9.iloc[-2]) <= float(ema21.iloc[-2])) and \
               (float(ema9.iloc[-1]) > float(ema21.iloc[-1])):
                
                uygunlar.append({"Sembol": ticker, "Fiyat": round(float(close.iloc[-1]), 2)})
                
        except: continue
        
    if uygunlar: st.dataframe(pd.DataFrame(uygunlar))
    else: st.warning("Bu listede Anayasa'ya uygun hisse yok. Yarın tekrar dene.")
