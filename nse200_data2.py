import pandas as pd
import numpy as  np
import yfinance as yf
import os 
nse100 = pd.read_csv('nifty200.csv')
#nifty_data = nse100[2].values
nifty_data = nse100['Symbol'].values

def snapshot():
    #with open('nifty100.csv') as f:
    for stock in nifty_data:
        #if "," not in line:
        #    continue
        symbol =  stock  #line.split(",")[2]
        #data = yf.download(symbol+'.NS', start="2020-01-01", end="2020-08-01")
        data = yf.download(symbol+'.NS', period='280d' )
        data.to_csv('daily/{}.csv'.format(symbol))
        print (symbol+'.NS')

    #!clear
    os. system('clear')

    return {"code": "success" }
nifty= yf.download('^NSEI',period='280d')
nifty.to_csv('daily/^NSEI.csv')


x=snapshot()

print(x)
#nifty_data.to_csv('select_stocks.csv', index=False)
