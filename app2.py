import streamlit as st
import yfinance as yf
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# --- WEB SAYFASI AYARLARI ---
st.set_page_config(page_title="Yatırım Anayasası v5", layout="centered")
st.title("Yatırım Anayasası - Altın Oran Tarayıcı")
st.markdown("**Duygulara yer yok. Sadece matematik ve kurallar.**")
st.markdown("S&P 500, Nasdaq 100 ve **S&P MidCap 400** endekslerindeki ~900 kaliteli hisse taranıyor...")
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

# --- 1. ADIM: KALİTELİ VE ORTA ÖLÇEKLİ HAVUZU ÇEKME ---
@st.cache_data(ttl=86400)
def endeks_hisselerini_getir():
    try:
        # 1. S&P 500 Listesi
        sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        sp500_table = pd.read_html(sp500_url, flavor='bs4')[0]
        sp500_tickers = sp500_table['Symbol'].tolist()
        
        # 2. Nasdaq 100 Listesi
        nasdaq_url = "https://en.wikipedia.org/wiki/Nasdaq-100"
        nasdaq_table = pd.read_html(nasdaq_url, flavor='bs4')[4]
        nasdaq_tickers = nasdaq_table['Ticker'].tolist()
        
        # 3. S&P MidCap 400 Listesi (Tam Yatırım Anayasasına Uygun Orta Ölçekli Şirketler)
        sp400_url = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"
        sp400_table = pd.read_html(sp400_url, flavor='bs4')[0]
        sp400_tickers = sp400_table['Symbol'].tolist()
        
        # Hepsini birleştir ve aynı olanları (mükerrer) çıkar
        tum_hisseler = list(set(sp500_tickers + nasdaq_tickers + sp400_tickers))
        temiz_hisseler = [t.replace('.', '-') for t in tum_hisseler if isinstance(t, str)]
        
        return sorted(temiz_hisseler)
    except:
        return ["AAPL", "MSFT", "AMZN", "NVDA", "SOFI", "PLTR", "RIVN", "F", "INTC", "CHWY", "U", "LCID"]

hisse_havuzu = endeks_hisselerini_getir()
st.info(f"Aktif Havuz: S&P 500 + Nasdaq 100 + S&P 400 ({len(hisse_havuzu)} Benzersiz Hisse)")

# --- 2. ADIM: TARAMA MEKANİZMASI ---
if st.button("900 Hisseyi Birden Tara"):
    uygun_hisseler = []
    
    ilerleme_barı = st.progress(0)
    durum_yazisi = st.empty()
    toplam_hisse = len(hisse_havuzu)
    
    for index, ticker in enumerate(hisse_havuzu):
        yuzde = int((index + 1) / toplam_hisse * 100)
        ilerleme_barı.progress(yuzde)
        durum_yazisi.text(f"Avlanıyor: {ticker} ({index+1}/{toplam_hisse})")
        
        try:
            df = yf.download(ticker, period="2mo", progress=False, show_errors=False)
            if df.empty or len(df) < 25: continue
            
            close = df['Close'].squeeze()
            high = df['High'].squeeze()
            low = df['Low'].squeeze()
            
            rsi = hesapla_rsi(close)
            stoch = hesapla_stokastik(high, low, close)
            ema9 = hesapla_ema(close, 9)
            ema21 = hesapla_ema(close, 21)
            
            son_kapanis = float(close.iloc[-1])
            son_ema9 = float(ema9.iloc[-1])
            son_ema21 = float(ema21.iloc[-1])
            onceki_ema9 = float(ema9.iloc[-2])
            onceki_ema21 = float(ema21.iloc[-2])
            
            # --- YATIRIM ANAYASASI ---
            kural_5 = son_kapanis <= 50
            kural_9_kesisim = (onceki_ema9 <= onceki_ema21) and (son_ema9 > son_ema21)
            
            son_7_gun_rsi = rsi.iloc[-7:]
            son_7_gun_stoch = stoch.iloc[-7:]
            kural_6_7_gecmis = (son_7_gun_rsi.min() <= 40) and (son_7_gun_stoch.min() <= 20)
            
            if kural_5 and kural_9_kesisim and kural_6_7_gecmis:
                uygun_hisseler.append({
                    "Sembol": ticker,
                    "Giriş": f"${round(son_kapanis, 2)}",
                    "Kâr Al (TP)": f"${round(son_kapanis * 1.25, 2)}",
                    "Stop (SL)": f"${round(son_kapanis * 0.95, 2)}",
                    "Dip RSI": round(float(son_7_gun_rsi.min()), 1),
                    "Dip Stoch": round(float(son_7_gun_stoch.min()), 1)
                })
        except:
            continue
            
    durum_yazisi.empty()
    ilerleme_barı.empty()
    st.divider()
    
    if uygun_hisseler:
        st.success(f"Dipten Dönüş Yapan {len(uygun_hisseler)} Orta/Büyük Ölçekli Cevher Bulundu!")
        st.dataframe(pd.DataFrame(uygun_hisseler), use_container_width=True)
    else:
        st.warning("900 hisse tarandı. Anayasa'ya uyan hisse bulunamadı. Disiplini koruyun ve bekleyin.")
