from flask import (
    Blueprint, redirect, render_template, flash
)


bp = Blueprint('analysis', __name__)
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


@bp.route('/analysis')
def analysis(symbol):
	if symbol in TOP_TRADED_SYMBOLS:
		return render_template('analysis.html') 

	if symbol != "":
		flash('No matching company listing found')
		return redirect('/')

	return render_template('index.html')
