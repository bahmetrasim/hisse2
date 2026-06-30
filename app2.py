import streamlit as st
import yfinance as yf
import pandas as pd
import time
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Anayasa v11 - Dev Tarayıcı", layout="centered")
st.title("Yatırım Anayasası v11")
st.markdown("900+ hisse için tam yetkili tarama modu.")

# Sabit listeniz (Sizin paylaştığınız liste)
FULL_LIST = [
    "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "AVGO", "TSLA", "META", "MU", "LLY", "BRK-B", "AMD", 
    "WMT", "JPM", "INTC", "V", "JNJ", "AMAT", "XOM", "LRCX", "CAT", "CSCO", "MA", "ABBV", "ORCL", 
    "COST", "BAC", "KLAC", "GE", "UNH", "KO", "HD", "PG", "CVX", "SNDK", "MS", "MRK", "GEV", "NFLX", 
    "GS", "PM", "PLTR", "PANW", "DELL", "TXN", "IBM", "MRVL", "WFC", "RTX", "LIN", "C", "AXP", "VZ", 
    "KO", "MCD", "JNJ", "PG", "UNH", "HD", "V", "MA", "ORCL", "CMCSA", "ABBV", "NEE", "LLY", "MRK", 
    "ABT", "PNC", "USB", "FITB", "KEY", "ZION", "HBAN", "RF", "CFG", "MTB", "WBA", "KHC", "GIS", 
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
    "URBN", "JWN", "M", "KSS", "BBY", "DKS", "FL", "BBBY", "GME", "AMC", "WYNN",
    "LVS", "MGM", "CZR", "PEN", "RCL", "CCL", "NCLH", "MAR", "HLT", "H", "IHG", "WH",
    "CHH", "BKNG", "EXPE", "TRIP", "ABNB", "UBER", "LYFT", "DASH", "MELI", "SE", "JD", "BIDU", 
    "PDD", "BABA", "NTES", "VIPS", "TME", "IQ", "TAL", "EDU", "BEKE", "KOS", "HES", "DVN", 
    "EOG", "COP", "PXD", "APA", "FANG", "CLR", "MUR", "NFX", "CXO", "COG", "RRC", "EQT", 
    "SWN", "WLL", "CHK", "QEP", "CNX", "CRK", "BRY", "ESTE", "LPI", "REI", "SM", "XEC"
]

if st.button("Taramayı Başlat"):
    uygunlar = []
    basarili_sayac = 0
    bar = st.progress(0)
    
    for i, ticker in enumerate(FULL_LIST):
        bar.progress(int((i+1)/len(FULL_LIST)*100))
        try:
            # Engellenmemek için süre
            time.sleep(0.5) 
            df = yf.download(ticker, period="2mo", interval="1d", progress=False, 
                             threads=False, user_agent='Mozilla/5.0')
            
            if len(df) < 25: continue
            
            basarili_sayac += 1
            close = df['Close'].squeeze()
            ema9 = close.ewm(span=9, adjust=False).mean()
            ema21 = close.ewm(span=21, adjust=False).mean()
            
            if (float(close.iloc[-1]) <= 50) and \
               (float(ema9.iloc[-2]) <= float(ema21.iloc[-2])) and \
               (float(ema9.iloc[-1]) > float(ema21.iloc[-1])):
                
                uygunlar.append({"Sembol": ticker, "Fiyat": round(float(close.iloc[-1]), 2)})
        except: continue
        
    st.write(f"Tarama bitti. {len(FULL_LIST)} hisse taranıp {basarili_sayac} tanesinden veri alındı.")
    if uygunlar: st.dataframe(pd.DataFrame(uygunlar))
    else: st.warning("Anayasa'ya uygun hisse yok. Sabır disiplindir.")
