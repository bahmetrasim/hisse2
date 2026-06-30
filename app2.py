import streamlit as st
import yfinance as yf
import pandas as pd
import time
import warnings
warnings.filterwarnings("ignore")

# --- 1. İNDİKATÖR HESAPLAMA FONKSİYONLARI ---
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

# --- 2. CHUNKER FONKSİYONU (Hata buradaydı, şimdi tanımlı) ---
def chunker(seq, size):
    for pos in range(0, len(seq), size):
        yield seq[pos:pos + size]

# --- 3. SABİT LİSTE ---
FULL_LIST = [
    "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "AVGO", "TSLA", "META", "MU", "LLY", "BRK.B", "AMD", "WMT", "JPM", "INTC", "V", "JNJ", "AMAT", "XOM", "LRCX", "CAT", "CSCO", "MA", "ABBV", "ORCL", "COST", "BAC", "KLAC", "GE", "UNH", "KO", "HD", "PG", "CVX", "SNDK", "MS", "MRK", "GEV", "NFLX", "GS", "PM", "PLTR", "PANW", "DELL", "TXN", "IBM", "MRVL", "WFC", "RTX", "LIN", "C", "AXP", "WDC", "APH", "GLW", "ANET", "STX", "QCOM", "AMGN", "ADI", "CRWD", "MCD", "PEP", "TMO", "NEE", "TMUS", "VZ", "APP", "DE", "BA", "DIS", "TJX", "ETN", "UNP", "WELL", "SCHW", "ABT", "GILD", "BLK", "UBER", "T", "ISRG", "BX", "HON", "BKNG", "PFE", "DHR", "CB", "CVS", "PGR", "CRM", "PLD", "VRT", "COP", "VRTX", "COF", "LOW", "PH", "MO", "SYK", "SPGI", "BMY", "SBUX", "LMT", "FTNT", "SO", "TT", "PWR", "HWM", "EQIX", "CDNS", "MDT", "NOW", "NEM", "BNY", "DUK", "PNC", "CMI", "MAR", "GD", "USB", "MNST", "DDOG", "WMB", "UPS", "FCX", "HOOD", "JCI", "WM", "ADP", "CEG", "CSX", "MCK", "CMCSA", "HCA", "ABNB", "RCL", "SNPS", "ELV", "SHW", "MMM", "KKR", "DASH", "ADBE", "EMR", "MRSH", "CME", "MCO", "ECL", "VLO", "ITW", "AMT", "ORLY", "COHR", "ACN", "HLT", "MDLZ", "MPC", "AEP", "TER", "FDX", "TDG", "CI", "CL", "SPG", "KMI", "NOC", "CRH", "INTU", "NSC", "AON", "NXPI", "URI", "TRV", "ICE", "EOG", "SLB", "GM", "FIX", "MSI", "PSX", "CIEN", "ROST", "CTAS", "LITE", "MPWR", "WBD", "APO", "RSG", "APD", "REGN", "GWW", "PCAR", "DLR", "BSX", "TFC", "ALL", "NKE", "DAL", "CARR", "SRE", "D", "KEYS", "AFL", "FLEX", "TGT", "TEL", "HPE", "TRGP", "AJG", "O", "CTVA", "PSA", "CAH", "OKE", "BKR", "F", "AME", "FAST", "COR", "ROK", "MET", "LHX", "ETR", "VST", "EW", "AZO", "EA", "FITB", "NUE", "XEL", "FANG", "MCHP", "EBAY", "OXY", "EXC", "DVN", "HUM", "STT", "TTWO", "CVNA", "DHI", "WAB", "GRMN", "XYZ", "KDP", "ODFL", "NDAQ", "AXON", "UAL", "YUM", "VTR", "CCL", "CMG", "LYV", "BDX", "IDXX", "ED", "AMP", "PEG", "ADSK", "MSCI", "JBL", "AIG", "SYY", "IBKR", "CBRE", "WEC", "COIN", "VMC", "PYPL", "IRM", "PRU", "PCG", "A", "ADM", "EME", "KVUE", "ON", "WAT", "KMB", "HIG", "HBAN", "HSY", "PAYX", "MTB", "ACGL", "MLM", "ROP", "Q", "KR", "CCI", "EQT", "STLD", "NTRS", "IR", "BIIB", "IQV", "DTE", "CNC", "AEE", "EXPE", "NRG", "EXR", "TDY", "LVS", "DOV", "NTAP", "ZTS", "WDAY", "SATS", "TPL", "TPR", "CFG", "RJF", "CASY", "CNP", "GEHC", "EIX", "ATO", "CINF", "VICI", "VEEV", "HAL", "EL", "KHC", "RMD", "MRNA", "XYL", "WSM", "FE", "PPL", "FICO", "HUBB", "ES", "OTIS", "JBHT", "PPG", "AVB", "WRB", "DXCM", "PHM", "AWK", "RF", "FISV", "CPRT", "MTD", "SYF", "EQR", "DG", "FSLR", "CBOE", "WST", "LUV", "KEY", "ARES", "WTW", "TROW", "SW", "RL", "CMS", "FFIV", "DGX", "VRSK", "DRI", "L", "PFG", "DLTR", "STZ", "LH", "CHD", "NI", "VRSN", "FDXF", "INCY", "LEN", "CHRW", "EXE", "VLTO", "BRO", "CPAY", "EXPD", "PKG", "BG", "SNA", "OMC", "STE", "HPQ", "AMCR", "TSN", "IP", "EVRG", "ROL", "LII", "FIS", "LNT", "DOW", "IFF", "GPN", "ULTA", "SMCI", "SBAC", "ESS", "VTRS", "EFX", "GIS", "FTV", "DD", "NVR", "CTSH", "INVH", "CDW", "BEN", "KIM", "GNRC", "WY", "AKAM", "CHTR", "LYB", "NDSN", "CF", "IEX", "BALL", "TSCO", "MAS", "HST", "MAA", "ZBH", "GPC", "ALB", "TXT", "BBY", "BR", "TKO", "GEN", "DOC", "J", "REG", "SWK", "DVA", "EG", "COO", "GL", "DECK", "HRL", "MKC", "AIZ", "SOLV", "PNW", "PTC", "UDR", "APTV", "LULU", "LDOS", "AVY", "ERIE", "BF.B", "PNR", "ZBRA", "RVTY", "MGM", "SJM", "ALLE", "TYL", "ALGN", "TRMB", "IVZ", "HAS", "CSGP", "APA", "CPT", "CLX", "GDDY", "PSKY", "HII", "BAX", "TECH", "CRL", "FRT", "BXP", "PODD", "AES", "SWKS", "FOXA", "FOX", "WYNN", "DPZ", "JKHY", "NCLH", "BLDR", "HSIC", "ARE", "NWSA", "UHS", "IT", "AOS", "TTD", "FDS", "TAP", "MOS", "CAG", 
    "NWS", "MTZ", "TWLO", "CRS", "MTSI", "MKSI", "ILMN", "CW", "ATI", "NVT", "ENTG", "FTI", "WWD", "ROIV", "STRL", "XPO", "P", "UTHR", "OKTA", "USFD", "SNX", "DKS", "SN", "AMKR", "ROKU", "ULS", "LSCC", "RBC", "BURL", "TTMI", "RS", "FN", "SITM", "H", "TLN", "APG", "PFGC", "EWBC", "ONTO", "BWXT", "RGLD", "NBIX", "ITT", "NLY", "CDE", "WCC", "VICR", "WSO", "NXT", "SGI", "WPC", "THC", "LAMR", "CLH", "DOCN", "PR", "TOL", "CSL", "MEDP", "VNOM", "PNFP", "DY", "DTM", "OVV", "JAZZ", "ARMK", "RRX", "CG", "SMTC", "JLL", "ALLY", "LECO", "UNM", "OHI", "CNH", "RPM", "AA", "RGA", "WMG", "TRU", "EVR", "NTNX", "RNR", "EXEL", "MLI", "BWA", "MOG.A", "RMBS", "AEIS", "CRBG", "SOLS", "GLPI", "DT", "SANM", "FNF", "COKE", "DINO", "TXRH", "CR", "KNX", "GGG", "OC", "ELS", "BROS", "EQH", "CCK", "PEN", "ALGM", "ELAN", "AIT", "WBS", "PINS", "AMH", "FHN", "WTS", "SPXC", "AAL", "WMS", "LAD", "CYTK", "VIAV", "AFG", "NYT", "BJ", "GMED", "CGNX", "LFUS", "SAIA", "ARWR", "BMRN", "AYI", "VMI", "EGP", "CART", "ARW", "WTRG", "AM", "WTFC", "UMBF", "AR", "SCI", "SF", "SEIC", "HL", "RYAN", "AAON", "DCI", "R", "ZION", "OGE", "ORI", "CACI", "BLD", "GWRE", "EHC", "GTLS", "JEF", "TKR", "ONB", "GME", "MUSA", "BRX", "FIVE", "SIRI", "SSB", "MP", "CFR", "OSK", "WLK", "CTRE", "CAVA", "SARO", "FCFS", "FLS", "TTC", "CNM", "COLB", "ENSG", "ADC", "CUBE", "HLI", "HALO", "BRKR", "WAL", "AMG", "BSY", "NNN", "ACM", "PRI", "KTOS", "AGCO", "SSD", "DOCU", "ALV", "RRC", "CBSH", "DAR", "IDA", "TEX", "FR", "VOYA", "ENS", "MANH", "VLY", "JHG", "ATR", "CHWY", "BIO", "MIDD", "HIMS", "RGEN", "REXR", "SFM", "KNSL", "CELH", "THG", "FLR", "TTEK", "STAG", "UGI", "NFG", "HXL", "BAH", "VNO", "PB", "CRUS", "KEX", "HQY", "AXTA", "NEU", "SLAB", "AVT", "CMC", "IDCC", "HR", "LNTH", "LSTR", "AVAV", "EXP", "FAF", "PPC", "AVTR", "FNB", "ST", "ORA", "GBCI", "GAP", "LEA", "ACI", "BYD", "LAD", "MSA", "NOV", "TMHC", "VFC", "CHRD", "RYN", "MSM", "WH", "SWX", "M", "CHDN", "GATX", "FND", "AN", "TXNM", "UBSI", "STWD", "FLG", "CROX", "MTDR", "DBX", "CHE", "FBIN", "HWC", "POR", "INGR", "ESAB", "ESNT", "MTG", "CVLT", "MORN", "KRG", "SIGI", "WFRD", "GXO", "HOMB", "ALK", "NJR", "BKH", "PCTY", "OZK", "LPX", "NOVT", "BC", "APPF", "PATH", "SON", "PBF", "PSN", "CAR", "DUOL", "RLI", "GNTX", "CLF", "AHR", "NXST", "UFPI", "TREX", "VAL", "ASB", "CHH", "PEGA", "VVV", "SHC", "GHC", "CUZ", "FFIN", "OGS", "DLB", "SLM", "SBRA", "SLGN", "KNF", "CNO", "MUR", "TNL", "HRB", "MTN", "SAIC", "WEX", "BBWI", "IBOC", "G", "CNX", "IPGP", "SR", "CBT", "BDC", "LIVN", "SYNA", "QLYS", "EPR", "WING", "FCN", "TCBI", "KRC", "NWE", "NVST", "OLLI", "FHI", "KBR", "HGV", "HLNE", "ELF", "CDP", "THO", "PLNT", "POST", "PII", "VNT", "OLED", "MAT", "ANF", "IRT", "SMG", "KBH", "EXLS", "FOUR", "YETI", "BCO", "DOCS", "LOPE", "BHF", "BILL", "NSA", "GEF", "HAE", "PVH", "AVNT", "OPCH", "MZTI", "COLM", "GPK", "RH", "ASH", "PK", "EXPO", "MMS", "CXT", "EEFT", "HOG", "VC", "KD", "WHR", "OLN", "CPRI", "XRAY", "GT", "SAM"
]
# --- 4. ARAYÜZ VE TARAMA ---
st.set_page_config(page_title="Anayasa v13 - Tam Filtreli", layout="centered")
st.title("Yatırım Anayasası v13")

if st.button("Taramayı Başlat"):
    uygunlar = []
    for paket in chunker(FULL_LIST, 50):
        for ticker in paket:
            try:
                time.sleep(0.5)
                df = yf.download(ticker, period="2mo", interval="1d", progress=False, threads=False, user_agent='Mozilla/5.0')
                if len(df) < 25: continue
                
                # İndikatörler
                close = df['Close'].squeeze()
                high = df['High'].squeeze()
                low = df['Low'].squeeze()
                rsi = hesapla_rsi(close)
                stoch = hesapla_stokastik(high, low, close)
                ema9 = close.ewm(span=9, adjust=False).mean()
                ema21 = close.ewm(span=21, adjust=False).mean()
                
                # Filtreler
                son_kapanis = float(close.iloc[-1])
                kural_5 = son_kapanis <= 50
                kural_9_kesisim = (float(ema9.iloc[-2]) <= float(ema21.iloc[-2])) and (float(ema9.iloc[-1]) > float(ema21.iloc[-1]))
                kural_6_7_gecmis = (rsi.iloc[-7:].min() <= 40) and (stoch.iloc[-7:].min() <= 20)
                
                if kural_5 and kural_9_kesisim and kural_6_7_gecmis:
                    uygunlar.append({"Sembol": ticker, "Fiyat": round(son_kapanis, 2)})
            except: continue
        time.sleep(10)
    
    if uygunlar: st.dataframe(pd.DataFrame(uygunlar))
    else: st.warning("Şu an Anayasa'ya uygun hisse yok.")
