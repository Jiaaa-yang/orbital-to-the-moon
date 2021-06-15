"""
Runner file to collect given data. Designed as a command line script
to collect different sets of data on different period.

Recommended usage:
    Call the script with a command line argument:
        'odd': writes mixed twitter data
        'even': writes financial twitter and reddit data
        'prices': writes prices data
    
    To prevent large amount of duplicates as a result of identical
    search queries, call the script on alternate days. Prices data span
    over 5 months period, so such data can be written when needed, or every
    5 months time

    Manually call the script on alternate days depending on a odd or even day
    of the month, or a task scheduler such as cronjob can be used
"""
from dotenv import load_dotenv
load_dotenv()

from data_collection.write_data.reddit_data import write_reddit_data
from data_collection.write_data.twitter_data import write_twitter_data
from data_collection.write_data.prices_data import write_prices_data
from data_collection.write_data.utility import create_logger
from threading import Thread
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
        if arg == "odd":
            # Get mixed: informative and financial tweets on odd days
            write_twitter_data(stock_symbols=TOP_TRADED_SYMBOLS, result_type="mixed", query_type="mixed", file="mixed_tweets_both.csv")
            write_twitter_data(stock_symbols=TOP_TRADED_SYMBOLS, result_type="popular", query_type="mixed", file="mixed_tweets_popular.csv")
            logger.info("=================LAST LOGGED: MIXED TWITTER DATA=================")
        elif arg == "even":
            # Get financial tweets and reddit posts on even days
            # Get reddit data on separate thread for better performance, since main thread 
            # has to wait for twitter api rate limit
            write_reddit_thread = Thread(target=write_reddit_data, args=(TOP_TRADED_SYMBOLS,))
            write_reddit_thread.start()
            write_twitter_data(stock_symbols=TOP_TRADED_SYMBOLS, result_type="mixed", query_type="financial", file="financial_tweets_both.csv")
            write_twitter_data(stock_symbols=TOP_TRADED_SYMBOLS, result_type="popular", query_type="financial", file="financial_tweets_popular.csv")
            write_reddit_thread.join()
            logger.info("=================LAST LOGGED: FINANCIAL TWITTER AND REDDIT DATA=================")
        elif arg == "prices":
            # Write prices data when needed, since data spans over a period of 5 months
            write_prices_data(TOP_TRADED_SYMBOLS)
            logger.info("=================LAST LOGGED: PRICES DATA=================")
        else:
            print("Invalid argument: must be one of 'odd', 'even' or 'prices'")


if __name__ == "__main__":
    main()