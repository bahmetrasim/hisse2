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
    ​"NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "AVGO", "TSLA", "META", "MU", "LLY", "BRK.B", 
    "AMD", "WMT", "JPM", "INTC", "V", "JNJ", "AMAT", "XOM", "LRCX", "CAT", "CSCO", "MA", "ABBV", "ORCL", 
    "COST", "BAC", "KLAC", "GE", "UNH", "KO", "HD", "PG", "CVX", "SNDK", "MS", "MRK", "GEV", "NFLX", "GS", 
    "PM", "PLTR", "PANW", "DELL", "TXN", "IBM", "MRVL", "WFC", "RTX", "LIN", "C", "AXP", "WDC", "APH", "GLW", 
    "ANET", "STX", "QCOM", "AMGN", "ADI", "CRWD", "MCD", "PEP", "TMO", "NEE", "TMUS", "VZ", "APP", "DE", 
    "BA", "DIS", "TJX", "ETN", "UNP", "WELL", "SCHW", "ABT", "GILD", "BLK", "UBER", "T", "ISRG", "BX", "HON", 
    "BKNG", "PFE", "DHR", "CB", "CVS", "PGR", "CRM", "PLD", "VRT", "COP", "VRTX", "COF", "LOW", "PH", "MO", 
    "SYK", "SPGI", "BMY", "SBUX", "LMT", "FTNT", "SO", "TT", "PWR", "HWM", "EQIX", "CDNS", "MDT", "NOW", "NEM", 
    "BNY", "DUK", "PNC", "CMI", "MAR", "GD", "USB", "MNST", "DDOG", "WMB", "UPS", "FCX", "HOOD", "JCI", "WM", 
    "ADP", "CEG", "CSX", "MCK", "CMCSA", "HCA", "ABNB", "RCL", "SNPS", "ELV", "SHW", "MMM", "KKR", "DASH", "ADBE", 
    "EMR", "MRSH", "CME", "MCO", "ECL", "VLO", "ITW", "AMT", "ORLY", "COHR", "ACN", "HLT", "MDLZ", "MPC", "AEP", "TER", 
    "FDX", "TDG", "CI", "CL", "SPG", "KMI", "NOC", "CRH", "INTU", "NSC", "AON", "NXPI", "URI", "TRV", "ICE", "EOG", 
    "SLB", "GM", "FIX", "MSI", "PSX", "CIEN", "ROST", "CTAS", "LITE", "MPWR", "WBD", "APO", "RSG", "APD", "REGN", "GWW", 
    "PCAR", "DLR", "BSX", "TFC", "ALL", "NKE", "DAL", "CARR", "SRE", "D", "KEYS", "AFL", "FLEX", "TGT", "TEL", "HPE", "TRGP", 
    "AJG", "O", "CTVA", "PSA", "CAH", "OKE", "BKR", "F", "AME", "FAST", "COR", "ROK", "MET", "LHX", "ETR", "VST", "EW", 
    "AZO", "EA", "FITB", "NUE", "XEL", "FANG", "MCHP", "EBAY", "OXY", "EXC", "DVN", "HUM", "STT", "TTWO", "CVNA", "DHI", 
    "WAB", "GRMN", "XYZ", "KDP", "ODFL", "NDAQ", "AXON", "UAL", "YUM", "VTR", "CCL", "CMG", "LYV", "BDX", "IDXX", "ED", 
    "AMP", "PEG", "ADSK", "MSCI", "JBL", "AIG", "SYY", "IBKR", "CBRE", "WEC", "COIN", "VMC", "PYPL", "IRM", "PRU", "PCG", 
    "A", "ADM", "EME", "KVUE", "ON", "WAT", "KMB", "HIG", "HBAN", "HSY", "PAYX", "MTB", "ACGL", "MLM", "ROP", "Q", "KR", 
    "CCI", "EQT", "STLD", "NTRS", "IR", "BIIB", "IQV", "DTE", "CNC", "AEE", "EXPE", "NRG", "EXR", "TDY", "LVS", "DOV", 
    "NTAP", "ZTS", "WDAY", "SATS", "TPL", "TPR", "CFG", "RJF", "CASY", "CNP", "GEHC", "EIX", "ATO", "CINF", "VICI", 
    "VEEV", "HAL", "EL", "KHC", "RMD", "MRNA", "XYL", "WSM", "FE", "PPL", "FICO", "HUBB", "ES", "OTIS", "JBHT", "PPG", 
    "AVB", "WRB", "DXCM", "PHM", "AWK", "RF", "FISV", "CPRT", "MTD", "SYF", "EQR", "DG", "FSLR", "CBOE", "WST", "LUV", 
    "KEY", "ARES", "WTW", "TROW", "SW", "RL", "CMS", "FFIV", "DGX", "VRSK", "DRI", "L", "PFG", "DLTR", "STZ", "LH", "CHD", 
    "NI", "VRSN", "FDXF", "INCY", "LEN", "CHRW", "EXE", "VLTO", "BRO", "CPAY", "EXPD", "PKG", "BG", "SNA", "OMC", "STE", 
    "HPQ", "AMCR", "TSN", "IP", "EVRG", "ROL", "LII", "FIS", "LNT", "DOW", "IFF", "GPN", "ULTA", "SMCI", "SBAC", "ESS", 
    "VTRS", "EFX", "GIS", "FTV", "DD", "NVR", "CTSH", "INVH", "CDW", "BEN", "KIM", "GNRC", "WY", "AKAM", "CHTR", "LYB", 
    "NDSN", "CF", "IEX", "BALL", "TSCO", "MAS", "HST", "MAA", "ZBH", "GPC", "ALB", "TXT", "BBY", "BR", "TKO", "GEN", "DOC", 
    "J", "REG", "SWK", "DVA", "EG", "COO", "GL", "DECK", "HRL", "MKC", "AIZ", "SOLV", "PNW", "PTC", "UDR", "APTV", "LULU", 
    "LDOS", "AVY", "ERIE", "BF.B", "PNR", "ZBRA", "RVTY", "MGM", "SJM", "ALLE", "TYL", "ALGN", "TRMB", "IVZ", "HAS", "CSGP", 
    "APA", "CPT", "CLX", "GDDY", "PSKY", "HII", "BAX", "TECH", "CRL", "FRT", "BXP", "PODD", "AES", "SWKS", "FOXA", "FOX", "WYNN", 
    "DPZ", "JKHY", "NCLH", "BLDR", "HSIC", "ARE", "NWSA", "UHS", "IT", "AOS", "TTD", "FDS", "TAP", "MOS", "CAG", "NWS"  
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
