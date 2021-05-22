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
TOP_TRADED_SYMBOLS = {'MARA', 'M', 'LGHL', 'SU', 'PALI', 'PSFE', 'ABR', 'QS', 'JD', 'ATOS', 'VZ', 'BSX', 'VIAC', 'TSLA', 'BB', 'NOK',
                     'INTC', 'AAPL', 'IQ', 'QCOM', 'AAL', 'EDU', 'OPGN', 'VTNR', 'RKT', 'VRM', 'FCX', 'TWTR', 'SOS', 'MS', 'EWZ', 'NKLA',
                     'F', 'BAC', 'NRZ', 'XLE', 'MDRR', 'TECK', 'BP', 'ING', 'AZN', 'IDEX', 'LI', 'MVIS', 'RBLX', 'AJG', 'GOLD', 'CSPR',
                     'TELL', 'FSR', 'JMIA', 'ACB', 'KO', 'NCLH', 'FB', 'CVX', 'SIRI', 'MGM', 'VIPS', 'T', 'TME', 'PLUG', 'RMED', 'APPS',
                     'WISH', 'SNAP', 'CPE', 'DKNG', 'DIS', 'RMO', 'DDD', 'IWM', 'UEC', 'WKHS', 'FUBO', 'CCIV', 'MT', 'TIGR', 'GE', 'ZNGA',
                     'HRTX', 'MU', 'SONO', 'NEM', 'JNJ', 'MSFT', 'EBON', 'BBVA', 'HBAN', 'NKE', 'FHN', 'BRFS', 'C', 'AMWL', 'UWMC', 'AMAT', 
                     'BILI', 'HL', 'OPEN', 'CPNG', 'NIO', 'ARRY', 'AHT', 'WFC', 'BMBL', 'FAMI', 'SQQQ', 'CTRM', 'SOXL', 'CRIS', 'ARKK', 'NERV',
                     'GLW', 'LUV', 'SPY', 'SAN', 'IBM', 'ITUB', 'SPCE', 'GNW', 'KEY', 'CCL', 'CSCO', 'FSLY', 'TSM', 'PTON', 'AUY', 'CS', 
                     'HPQ', 'LMND', 'FSM', 'GSK', 'LTHM', 'CNHI', 'AGNC', 'SID', 'TAL', 'AEG', 'LU', 'PYPL', 'EXK', 'UAL', 'PAAS', 'MRK', 
                     'CAN', 'XOM', 'UBER', 'ET', 'AR', 'WY', 'OCGN', 'HAL', 'NVDA', 'X', 'SNDL', 'BNGO', 'BNTC', 'IHT', 'GGB', 'RIG', 'BIDU', 
                     'SRNG', 'ON', 'FTEK', 'OXY', 'NLY', 'COIN', 'BBD', 'COP', 'TQQQ', 'PINS', 'DAL', 'SLB', 'CLF', 'SI', 'PLTR', 'HAE', 'KMI', 
                     'RIOT', 'FCEL', 'EYES', 'MRO', 'XPEV', 'BABA', 'BOX', 'EEM', 'AMC', 'BA', 'PBR', 'PSTG', 'UUUU', 'BIL', 'KOS', 'TLRY', 'FUTU', 
                     'PG', 'CMCSA', 'LHDX', 'AUTL', 'AMD', 'VALE', 'XLF', 'QQQ', 'JPM', 'SKLZ', 'GEVO', 'GME', 'SQ', 'UMC', 'KGC', 'NNDM', 'PFE',
                     'MRNA', 'GM', 'SNOW'}

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