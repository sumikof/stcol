from dataclasses import dataclass
import enum


class OvrIndex(enum.Enum):
    DJI = '^DJI'  # Dow Jones Industrial Average
    DJT = '^DJT'  # , 'Dow Jones Trnsport
    DJU = '^DJU'  # Dow Jones Utility Average
    BANK = '^BANK'  # NASDAQ Bank
    IXCO = '^IXCO'  # NASDAQ Computer
    NDX = '^NDX'  # NASDAQ-100
    NBI = '^NBI'  # NASDAQ Biotechnology
    NDXT = '^NDXT'  # NASDAQ 100 Technology
    INDS = '^INDS'  # NASDAQ Industrial
    INSR = '^INSR'  # NASDAQ Insurance
    OFIN = '^OFIN'  # NASDAQ Other Finance
    IXTC = '^IXTC'  # NASDAQ Telecommunications
    TRAN = '^TRAN'  # NASDAQ Transportation
    NYY = '^NYY'  # NYSE TMT INDEX
    NYI = '^NYI'  # NYSE INTL 100 INDEX
    NY = '^NY'  # NYSE US 100 INDEX
    NYL = '^NYL'  # NYSE NY World Leader Index
    XMI = '^XMI'  # NYSE ACRA Major Market Index
    OEX = '^OEX'  # S&P 100 Index
    GSPC = '^GSPC'  # S&P 500 Index
    HSI = '^HSI'  # Hang Seng Index
    FCHI = '^FCHI'  # CAC 40
    BVSP = '^BVSP'  # IBOVESPA
    N225 = '^N225'  # Nikkei 225
    RUA = '^RUA'  # Russel 3000
    XSX = '^XAX'  # NY AMEX Composit Index
    SOX = '^SOX'  # PHLX Semiconductor Index
    DXY = 'DX-Y.NYB'  # US Dollar/USDX - Index - Cash')


class CmdFuture(enum.Enum):
    ES_F = 'ES=F'  # S&P Futures
    YM_F = 'YM=F'  # Dow Futures
    NQ_F = 'NQ=F'  # Nasdaq Futures
    RTY_F = 'RTY=F'  # Russell 2000 Futures
    ZB_F = 'ZB=F'  # U.S. Treasury Bond Futures,Dec-
    ZN_F = 'ZN=F'  # 10-Year T-Note Futures,Dec-2021
    ZF_F = 'ZF=F'  # Five-Year US Treasury Note Futu
    ZT_F = 'ZT=F'  # 2-Year T-Note Futures,Dec-2021
    GC_F = 'GC=F'  # Gold
    MGC_F = 'MGC=F'  # Micro Gold Futures,Feb-2022
    SI_F = 'SI=F'  # Silver
    SIL_F = 'SIL=F'  # Micro Silver Futures,Dec-2021
    PL_F = 'PL=F'  # Platinum Jan 22
    HG_F = 'HG=F'  # Copper Dec 21
    PA_F = 'PA=F'  # Palladium Mar 22
    CL_F = 'CL=F'  # Crude Oil
    HO_F = 'HO=F'  # Heating Oil Dec 21
    NG_F = 'NG=F'  # Natural Gas Dec 21
    RB_F = 'RB=F'  # RBOB Gasoline Dec 21
    BZ_F = 'BZ=F'  # Brent Crude Oil Last Day Financ
    B0_F = 'B0=F'  # Mont Belvieu LDH Propane (OPIS)
    ZC_F = 'ZC=F'  # Corn Futures,Mar-2022
    ZO_F = 'ZO=F'  # Oat Futures,Mar-2022
    KE_F = 'KE=F'  # KC HRW Wheat Futures,Dec-2021
    ZR_F = 'ZR=F'  # Rough Rice Futures,Jan-2022
    ZM_F = 'ZM=F'  # Soybean Meal Futures,Jan-2022
    ZL_F = 'ZL=F'  # Soybean Oil Futures,Jan-2022
    ZS_F = 'ZS=F'  # Soybean Futures,Jan-2022
    GF_F = 'GF=F'  # Feeder Cattle Futures,Jan-2022
    HE_F = 'HE=F'  # Lean Hogs Futures,Dec-2021
    LE_F = 'LE=F'  # Live Cattle Futures,Dec-2021
    CC_F = 'CC=F'  # Cocoa Mar 22
    KC_F = 'KC=F'  # Coffee Mar 22
    CT_F = 'CT=F'  # Cotton Mar 22
    LBS_F = 'LBS=F'  # Lumber Jan 22
    OJ_F = 'OJ=F'  # Orange Juice Jan 22
    SB_F = 'SB=F'  # Sugar #11 Mar 22


class OvrEtf(enum.Enum):
    DIA = 'DIA'
    SPY = 'SPY'
    QQQ = 'QQQ'
    IBB = 'IBB'
    XLV = 'XLV'
    IWM = 'IWM'
    EEM = 'EEM'
    EFA = 'EFA'
    XLP = 'XLP'
    XLY = 'XLY'
    ITB = 'ITB'
    XLU = 'XLU'
    XLF = 'XLF'
    VGT = 'VGT'
    VT = 'VT'
    FDN = 'FDN'
    IWO = 'IWO'
    IWN = 'IWN'
    IYF = 'IYF'
    XLK = 'XLK'
    XOP = 'XOP'
    USMV = 'USMV'
    BAB = 'BAB'
    GLD = 'GLD'
    VNQ = 'VNQ'
    SCHH = 'SCHH'
    IYR = 'IYR'
    XLRE = 'XLRE'
    AGG = 'AGG'
    BND = 'BND'
    LQD = 'LQD'
    VCSH = 'VCSH'
    VCIT = 'VCIT'
    JNK = 'JNK'
    JETS = 'JETS'


class BondYields(enum.Enum):
    TNX = '^TNX'
    FVX = '^FVX'
    TYX = '^TYX'


class ExchangeRate(enum.Enum):
    USD_JPY = 'JPY=X'
    EUR_USD = 'EURUSD=X'
    GBP_USD = 'GBPUSD=X'
    USD_CHF = 'CHF=X'
    AUD_USD = 'AUDUSD=X'
    NZD_USD = 'NZDUSD=X'
    USD_CAD = 'CAD=X'
    USD_CNH = 'CNH=X'


@dataclass
class Stock:
    name: str
    value: str

    def __init__(self, code, name=''):
        self.value = code
        self.name = name


class _DomStockBase:
    _symbols = []

    def __getitem__(self, index):
        return self.symbols[index]

    def __len__(self):
        return len(self.symbols)

    @property
    def symbols(self):
        if len(self._symbols) == 0:
            import market.edinet
            self._symbols = sorted(market.edinet.kabu(), key=lambda x: x.value)
        return self._symbols


DomStock = _DomStockBase()
