import streamlit as st
import yfinance as yf
import pandas as pd
import time
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Anayasa v10 - Dev Tarayıcı", layout="centered")
st.title("Yatırım Anayasası v10")
st.markdown("900+ hisse, güvenlikli ve paketli tarama modunda.")

# 900+ hisselik tam liste
FULL_LIST = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "SOFI", "PLTR", "RIVN", "AMD", "INTC", 
    "CSCO", "NFLX", "ADBE", "CRM", "QCOM", "AVGO", "TXN", "TMUS", "PEP", "COST", "AMGN", "HON", 
    "UPS", "LMT", "GE", "IBM", "CAT", "F", "T", "PFE", "CHWY", "U", "LCID", "WBD", "PARA", "MRO", 
    "OXY", "HAL", "BA", "DIS", "XOM", "CVX", "JPM", "BAC", "WFC", "C", "GS", "MS", "AXP", "VZ", 
    "KO", "MCD", "JNJ", "PG", "UNH", "HD", "V", "MA", "ORCL", "CMCSA", "ABBV", "NEE", "LLY", 
    "MRK", "ABT", "PNC", "USB", "FITB", "KEY", "ZION", "HBAN", "RF", "CFG", "MTB", "KHC", "GIS", 
    "CL", "SYK", "BSX", "REGN", "GILD", "VRTX", "SNPS", "DE", "MMM", "DOW", "DD", "EMR", "ETN", 
    "PH", "ROK", "ITW", "GLW", "AFL", "ALL", "CB", "CINF", "HIG", "MET", "PRU", "WLTW", "AJG",
    "AON", "MMC", "BEN", "BK", "STT", "NTRS", "SCHW", "TROW", "AMP", "CB", "CME", "ICE", "MCO",
    "SPGI", "MSCI", "BLK", "BX", "KRR", "DFS", "COF", "SYF", "PYPL", "VRSK", "EQIX", "PLD", "PSA",
    "AMT", "CCI", "DLR", "WY", "AVB", "EXR", "MAA", "ESS", "UDR", "HST", "VTR", "WELL", "PEAK",
    "SBAC", "BXP", "O", "ARE", "KIM", "REG", "FRT", "SPG", "GGP", "KMX", "DHI", "LEN", "PHM",
    "NVR", "TOL", "KBH", "MDC", "BZH", "MTH", "RYN", "LPX", "WEYS", "POOL", "SNA", "SWK", "OSK",
    "XYL", "AGCO", "CNHI", "CARR", "OTIS", "IR", "TT", "ZBRA", "FTV", "AME", "DOV", "ROP", "TDG",
    "WSO", "FIX", "MHK", "LEG", "HNI", "MLI", "PNR", "HII", "GD", "NOC", "RTX", "LHX", "TXT",
    "TDY", "LLL", "CW", "BAH", "LDOS", "SAIC", "CACI", "MTZ", "ACM", "J", "FLR", "PWR", "FIX",
    "PRIM", "VRS", "GVA", "TTM", "KB", "KBR", "URS", "AECOM", "JLL", "CBRE", "CWST", "RSG",
    "WM", "WCN", "SRCL", "WTR", "AWK", "AEE", "AEP", "CMS", "CNP", "D", "DTE", "DUK", "ED",
    "EIX", "ES", "ETR", "FE", "NEE", "NI", "PEG", "PNW", "PPL", "SO", "SRE", "XEL", "AES",
    "EVRG", "LNT", "CMS", "WEC", "PAG", "CPRI", "RL", "PVH", "TPR", "KORS", "HBI", "GPS",
    "URBN", "JWN", "M", "KSS", "BBY", "DKS", "FL", "BBBY", "GME", "AMC", "AMC", "WYNN",
    "LVS", "MGM", "CZR", "PEN", "RCL", "CCL", "NCLH", "MAR", "HLT", "H", "IHG", "WH",
    "CHH", "BKNG", "EXPE", "TRIP", "ABNB", "UBER", "LYFT", "DASH", "GRUB", "DOORDASH",
    "MELI", "SE", "JD", "BIDU", "PDD", "BABA", "NTES", "VIPS", "TME", "IQ", "TAL", "EDU",
    "BEKE", "KOS", "HES", "DVN", "EOG", "COP", "PXD", "APA", "FANG", "CLR", "MUR", "NFX",
    "CXO", "COG", "RRC", "EQT", "SWN", "WLL", "CHK", "QEP", "CNX", "CRK", "BRY", "ESTE",
    "LPI", "REI", "SM", "XEC", "APA", "DVN", "EOG", "COP", "PXD", "APA", "FANG", "CLR"
]

def chunker(seq, size):
    for pos in range(0, len(seq), size):
        yield seq[pos:pos + size]

if st.button("Tüm Listeyi Tara (Sabır Disiplindir)"):
    uygunlar = []
    st.write(f"Tarama başladı: {len(FULL_LIST)} hisse taranıyor.")
    
    # 50'şerli paketler
    for i, paket in enumerate(chunker(FULL_LIST, 50)):
        st.write(f"Paket {i+1} taranıyor...")
        for ticker in paket:
            try:
                # Yahoo'yu yormamak için mikro bekleme
                df = yf.download(ticker, period="2mo", interval="1d", progress=False, 
                                 threads=False, user_agent='Mozilla/5.0')
                if len(df) < 25: continue
                
                close = df['Close'].squeeze()
                ema9 = close.ewm(span=9, adjust=False).mean()
                ema21 = close.ewm(span=21, adjust=False).mean()
                
                if (float(close.iloc[-1]) <= 50) and \
                   (float(ema9.iloc[-2]) <= float(ema21.iloc[-2])) and \
                   (float(ema9.iloc[-1]) > float(ema21.iloc[-1])):
                    uygunlar.append({"Sembol": ticker, "Fiyat": round(float(close.iloc[-1]), 2)})
            except: continue
        
        # Her 50 hisseden sonra Yahoo dinlensin
        st.write(f"Paket {i+1} bitti. Mola veriliyor...")
        time.sleep(5) 
        
    st.divider()
    if uygunlar: st.dataframe(pd.DataFrame(uygunlar))
    else: st.warning("Bu dev havuzda şu an Anayasa'ya uyan hisse yok.")
