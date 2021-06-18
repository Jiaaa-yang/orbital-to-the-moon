"""Runner module to collect data from APIs to store into csv files

Module designed as command line script which can collect different data
based on the frequencies they need to be updated. Can be called with either
'tweets' or 'prices' as a command line argument.

Recommended usage:
    Call the script with a command line argument:
        'tweets': Writes financial twitter data
        'prices': Writes prices data
    
    To prevent large amount of duplicates as a result of identical
    search queries, collect the twitter data once a day.
    Since the prices data span over a 5 months period, such data
    can be written when needed.

    Manually call the script daily or use a task scheduler like cronjob

"""
from write_data.twitter_data import write_twitter_data
from write_data.prices_data import write_prices_data
from write_data.utility import create_logger
import sys


# List of top traded/most active symbols to get data for
TOP_TRADED_SYMBOLS = {'AUY', 'F', 'NAKD', 'NCLH', 'ET', 'TJX', 'CS', 'AGNC', 'FAMI', 'CPE', 'CRIS', 'GSAT', 'GME', 'OPGN',
                      'NIO', 'KR', 'ON', 'BILI', 'AAL', 'FUTU', 'GEVO', 'PSTG', 'KGC', 'SCHW', 'ABT', 'XLF', 'MPW', 'NNDM',
                      'TPR', 'TSLA', 'AZN', 'MRVL', 'BABA', 'MOSY', 'SONO', 'ABR', 'HRTX', 'WY', 'TFC', 'LUMN', 'VST', 'CSPR',
                      'EXK', 'RLX', 'BIDU', 'HIMX', 'MPC', 'NERV', 'WPG', 'BRFS', 'GOTU', 'T', 'UWMC', 'KOS', 'PEAK', 'CLDR',
                      'RMED', 'FSR', 'UEC', 'TQQQ', 'BSX', 'CLNE', 'AR', 'MARA', 'SRNE', 'SID', 'TLRY', 'VTRS', 'CX', 'ADMP',
                      'GFI', 'AES', 'VIPS', 'SAN', 'BP', 'IHT', 'NOK', 'MU', 'EDU', 'TRGP', 'FSM', 'WISH', 'STAY', 'DIS', 'HL',
                      'SPY', 'ARRY', 'C', 'FHN', 'BBBY', 'BMY', 'FCX', 'MO', 'M', 'QFIN', 'MGM', 'MS', 'ORCL', 'UAL', 'DOCU', 'BBVA',
                      'IWM', 'INFY', 'CPNG', 'CVE', 'SOS', 'CCIV', 'ACST', 'PBR', 'GNW', 'IPOE', 'BNTC', 'MOS', 'LHDX', 'VRM', 'ENB', 'WFC',
                      'UMC', 'LUV', 'MRK', 'ACB', 'AMXVF', 'CNHI', 'QCOM', 'SOXL', 'NLY', 'IQ', 'CCL', 'CSCO', 'MVIS', 'CAN', 'SNAP', 'CMCSA',
                      'ZNGA', 'EWZ', 'AEG', 'CLOV', 'NCTY', 'NOKPF', 'GOLD', 'SNDL', 'COIN', 'BA', 'LEDS', 'PD', 'ATOS', 'VIAC', 'TNXP', 'CLF',
                      'MT', 'SPCE', 'EYES', 'NKLA', 'SYF', 'GLW', 'STLA', 'PSFE', 'NUAN', 'FTEK', 'HPQ', 'ABNB', 'PAAS', 'JBLU', 'HAL', 'PALI',
                      'JD', 'DKNG', 'AHT', 'ITUB', 'LMND', 'SLB', 'DISCA', 'TIGR', 'BOX', 'IDEX', 'GILD', 'KEY', 'PG', 'ERIC', 'JPM', 'HBAN',
                      'DAL', 'MRO', 'UUUU', 'PSTH', 'GGB', 'OXY', 'FEYE', 'RIDE', 'GM', 'RF', 'PLTR', 'FUBO', 'AMC', 'COG', 'AAPL', 'LI', 'OPEN',
                      'VALE', 'UPST', 'GSK', 'DBX', 'WKHS', 'SDC', 'SQ', 'CRWD', 'LTHM', 'JMIA', 'DDD', 'ZOM', 'QQQ', 'SI', 'NKE', 'EEM', 'DVN',
                      'XOM', 'RIG', 'INTC', 'BAC', 'WMB', 'TAL', 'KO', 'FB', 'FSLY', 'GPS', 'SQQQ', 'AMAT', 'X', 'HPE', 'JNJ', 'VZ', 'NEE', 'QS',
                      'PTON', 'ABEV', 'AMWL', 'CLNY', 'MDRR', 'BBD', 'FTI', 'ZM', 'SRNG', 'CRM', 'PBR-A', 'VTNR', 'COP', 'PCG', 'UBER', 'TWTR', 'AJG',
                      'CTRM', 'SENS', 'ARKK', 'BMBL', 'TSM', 'LVS', 'ING', 'XPEV', 'MRNA', 'IBM', 'AMCR', 'PYPL', 'PFE', 'EBON', 'GE', 'PINS', 'HAE',
                      'SU', 'RBLX', 'PLUG', 'BNGO', 'BIL', 'TME', 'TEVA', 'NEM', 'SIRI', 'AUTL', 'NVDA', 'FCEL', 'NRZ', 'LGHL', 'SWN', 'LU', 'KMI',
                      'RIOT', 'TELL', 'LPTH', 'MSFT', 'SKLZ', 'CVX', 'AMD', 'UAA', 'EBAY', 'RMO', 'AEO', 'MAC', 'VEON', 'OCGN', 'XLE', 'TECK', 'SNOW',
                      'APA', 'RKT', 'BKR', 'BB', 'APPS'}

def main():
    if len(sys.argv) != 2:
        print("Enter one command line argument")
    else:
        arg = sys.argv[1].lower()
        logger = create_logger(__name__)
        if arg == "tweets":
            write_twitter_data(stock_symbols=TOP_TRADED_SYMBOLS, result_type="mixed", file="financial_tweets_mixed.csv")
            write_twitter_data(stock_symbols=TOP_TRADED_SYMBOLS, result_type="popular", file="financial_tweets_popular.csv")
            logger.info("=================LAST LOGGED: TWITTER DATA=================")
        elif arg == "prices":
            # Write prices data when needed, since data spans over a period of 5 months
            write_prices_data(TOP_TRADED_SYMBOLS)
            logger.info("=================LAST LOGGED: PRICES DATA=================")
        else:
            print("Invalid argument: must be either 'tweets' or 'prices'")


if __name__ == "__main__":
    main()
