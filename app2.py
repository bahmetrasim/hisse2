import streamlit as st
import yfinance as yf
import pandas as pd
import time
import warnings
warnings.filterwarnings("ignore")

# --- WEB SAYFASI AYARLARI ---
st.set_page_config(page_title="Yatırım Anayasası v6", layout="centered")
st.title("Yatırım Anayasası - Global Tarayıcı")
st.markdown("900+ hisse taranıyor. Sistem engellere karşı korunmalı moddadır.")
st.divider()

# --- SAF MATEMATİKSEL İNDİKATÖR FONKSİYONLARI ---
def hesapla_ema(veri, periyot):
    return veri.ewm(span=periyot, adjust=False).mean()

def hesapla_rsi(veri, periyot=14):
    fark = veri.diff()
    yukari = fark.clip(lower=0)
    asagi = -1 * fark.clip(upper=0)
    ema_yukari = yukari.ewm(com=periyot-1, adjust=False).mean()
    ema_asagi = asagi.ewm(com=periyot-1, adjust=False).mean()
    rs = ema_yukari / ema_asagi
    return 100 - (100 / (1 + rs))

def hesapla_stokastik(yuksek, dusuk, kapanis, periyot=14):
    en_dusuk = dusuk.rolling(window=periyot).min()
    en_yuksek = yuksek.rolling(window=periyot).max()
    return 100 * ((kapanis - en_dusuk) / (en_yuksek - en_dusuk))

# --- HAVUZU HAZIRLA ---
@st.cache_data(ttl=86400)
def endeks_hisselerini_getir():
    try:
        # Wikipedia verilerini çek
        sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]['Symbol'].tolist()
        nasdaq = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[4]['Ticker'].tolist()
        sp400 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_400_companies")[0]['Symbol'].tolist()
        
        tum = sorted(list(set([t.replace('.', '-') for t in sp500 + nasdaq + sp400])))
        return tum
    except:
        return ["AAPL", "MSFT", "SOFI", "PLTR", "RIVN", "F", "INTC", "CHWY", "U", "LCID"]

hisse_havuzu = endeks_hisselerini_getir()
st.info(f"Tarama Havuzu Hazır: {len(hisse_havuzu)} Benzersiz Hisse")

# --- TARAMA MOTORU ---
if st.button("900 Hisseyi Tara"):
    uygun_hisseler = []
    basarili, hata = 0, 0
    
    ilerleme = st.progress(0)
    bilgi = st.empty()
    
    for i, ticker in enumerate(hisse_havuzu):
        ilerleme.progress(int((i+1)/len(hisse_havuzu)*100))
        bilgi.text(f"Taranıyor: {ticker}")
        
        try:
            # Engellenmemek için bekleme süresi
            time.sleep(0.5) 
            df = yf.download(ticker, period="2mo", interval="1d", progress=False, show_errors=False)
            
            if df.empty or len(df) < 25:
                hata += 1
                continue
            
            basarili += 1
            close = df['Close'].squeeze()
            high = df['High'].squeeze()
            low = df['Low'].squeeze()
            
            rsi = hesapla_rsi(close)
            stoch = hesapla_stokastik(high, low, close)
            ema9 = hesapla_ema(close, 9)
            ema21 = hesapla_ema(close, 21)
            
            # KONTROLLER
            if float(close.iloc[-1]) <= 50:
                if (float(ema9.iloc[-2]) <= float(ema21.iloc[-2])) and (float(ema9.iloc[-1]) > float(ema21.iloc[-1])):
                    if (rsi.iloc[-7:].min() <= 40) and (stoch.iloc[-7:].min() <= 20):
                        uygun_hisseler.append({
                            "Sembol": ticker,
                            "Giriş": round(float(close.iloc[-1]), 2),
                            "Kâr Al": round(float(close.iloc[-1]) * 1.25, 2),
                            "Stop": round(float(close.iloc[-1]) * 0.95, 2)
                        })
        except:
            hata += 1
            continue
            
    st.divider()
    st.info(f"İşlem bitti: {basarili} başarı, {hata} hata.")
    
    if uygun_hisseler:
        st.dataframe(pd.DataFrame(uygun_hisseler))
    else:
        st.warning("Bugün Anayasa'ya uygun hisse yok. Sabır disiplindir.")
