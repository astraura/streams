import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import ta
import yfinance as yf
import time
import datetime as dt
from scipy import stats
from statistics import mean

path = 'yearly/'
#driver = webdriver.Chrome()
#chrome_options.add_argument("--headless")


nifty_data= pd.read_csv('nifty200.csv')
tickers = nifty_data['Symbol'].to_list()
df = pd.DataFrame()
df = pd.read_csv('yearly/ZEEL.csv')
df_new = yf.download('ZEEL.NS', period='1d' )
latest = df_new.index.values[0]
last_update = pd.to_datetime(df[-1:]['Date'].values[0])

def chart(df):
    candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
    df['20sma'] = df['Close'].rolling(window=20).mean()
    df['50sma'] = df['Close'].rolling(window=50).mean()

    sma20 = go.Scatter(x=df['Date'], y=df['20sma'], name='SMA20', line={'color': 'red'})
    sma50 = go.Scatter(x=df['Date'], y=df['50sma'], name='SMA50', line={'color': 'green'})

    fig = go.Figure(data=[candlestick, sma20, sma50])
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    #fig.show()
    return fig
def chart2(df):
    mfi = ta.volume.money_flow_index(df['High'],df['Low'],df['Close'],df['Volume'], window=10)
    mfi3 = mfi3 = ta.trend.sma_indicator(mfi, window=3)
    prices = df['Close']
    macd = ta.trend.macd(prices, window_slow = 26, window_fast = 12)
    macds =ta.trend.macd_signal(prices, window_slow = 26, window_fast = 12)
    macdh =ta.trend.macd_diff(prices, window_slow = 26, window_fast = 12)    
    rsi10=ta.momentum.rsi(prices, window=10, )


    rsi10line = go.Scatter(x=df['Date'], y=rsi10, name='RSI 10 line', line={'color': 'blue'})
    mfi10line = go.Scatter(x=df['Date'], y=mfi, name='MFI 10 line', line={'color': 'red'})
    mfi3line =  go.Scatter(x=df['Date'], y=mfi3, name='MFI 3SMA line', line={'color': 'orange'})
    fig2 = go.Figure(data=[rsi10line, mfi10line, mfi3line])

    fig2.layout.xaxis.type = 'category'
    fig2.layout.xaxis.rangeslider.visible = False
    #fig2.show()
    return fig2
#chart2(df)


def snapshot():
    my_bar = st.progress(0)
    i=1
    #with open('nifty100.csv') as f:

    for stock in tickers:
        with st.spinner('Wait.. {}'.format(stock)):

        #st.spinner('Wait..updated.' + symbol)
       
        #if "," not in line:
        #    continue
            symbol =  stock  #line.split(",")[2]
            #data = yf.download(symbol+'.NS', start="2020-01-01", end="2020-08-01")
            data = yf.download(symbol+'.NS', period='5y' )
            data.to_csv('yearly/{}.csv'.format(symbol))
            my_bar.progress( round(i/len(nifty_data)*100))
            i+=1
            #if i>10:
            #    break
    st.success("Done!..")
            

        #st.write (symbol+'.NS')

    nifty= yf.download('^NSEI',period='5y')
    nifty   .to_csv('yearly/^NSEI.csv')

    return {"Updation: ": "Success!" }

def snapshot2():

    
    return "Gompada"




def returns():
    
    stocks = pd.read_csv('nifty200.csv')['Symbol']
    #mycolumns=['Symbol', '1dretAnnualized','1y','6m','3m','1m',]
    mycolumns = ["Symbol","Price" ,'1dretAnnualized', "y1_return","y1_return_percentile" , "m6_return","m6_return_percentile","m3_return","m3_return_percentile","m1_return","m1_return_percentile","HQM_Score"]

    data =pd.DataFrame(columns=mycolumns)
    #data['Symbol'] = stocks
    #One year return
    for i in stocks.index:
        df = pd.read_csv(path+stocks[i]+'.csv')
        df['change']= df['Adj Close'].pct_change()
        yrate =  df.loc[-250:,'change'].mean()*252
        data.loc[i,'Symbol'] = stocks[i]
        data.loc[i,'Price'] = df.loc[len(df)-1,'Adj Close']
        data.loc[i, '1dretAnnualized']= yrate
        data.loc[i, 'y1_return'] = df.loc[len(df)-1,'Adj Close']/df.loc[len(df)-252,'Adj Close']-1
        data.loc[i, 'm6_return'] = df.loc[len(df)-1,'Adj Close']/df.loc[len(df)-130,'Adj Close']-1 
        data.loc[i, 'm3_return'] = df.loc[len(df)-1,'Adj Close']/df.loc[len(df)-70,'Adj Close']-1    
        data.loc[i, 'm1_return'] = df.loc[len(df)-1,'Adj Close']/df.loc[len(df)-30,'Adj Close']-1

    time_period = ["y1","m6","m3","m1"]
    #time_period = ['1yReturn','6mReturn','3mReturn','1mReturn']

    for row in data.index:
        for time in time_period:
            data.at[row,f"{time}_return_percentile"] = float(stats.percentileofscore(data[f"{time}_return"],data.at[row,f"{time}_return"]))
    for row in data.index:
        l = []
        for time in time_period:
            l.append(data.at[row,f"{time}_return_percentile"])
        avg = mean(l)
        data.at[row,"HQM_Score"] = avg
    #data = data.round(2)
    data.to_csv('Nifty portfolio returns.csv')

    return data
def sorted_returns(data):
    data = data.sort_values("HQM_Score",ascending=False,ignore_index=True)[:15]
    data.to_csv("Nifty_Portfolio_Momentum.csv")
    return data

     
def get_fundas(df):
    vdf = df.copy()
    vdf.dropna()
    index_names = vdf[ vdf['ROE%'] == 0].index
    vdf.drop(index_names, inplace = True)
    index_names = vdf[ vdf['P/E'] == 0].index
    vdf.drop(index_names, inplace = True)

    vdf['PE/ROE']=vdf['P/E']/vdf['ROE%']
    
    return vdf

def ranked_fundas(vdf):
    vdfselect0 = vdf[vdf['PE/ROE']<.5*vdf['PE/ROE'].mean()]
    vdfselect = vdfselect0.copy()
    vdfselect['NPM%_percentile'] = pd.Series(np.random.randn(len(vdfselect)), index=vdfselect.index)
    vdfselect['ROE%_percentile'] = pd.Series(np.random.randn(len(vdfselect)), index=vdfselect.index)
    vdfselect['PE/ROE_percentile'] = pd.Series(np.random.randn(len(vdfselect)), index=vdfselect.index)
    vdfselect['HQV_Score']=pd.Series(np.random.randn(len(vdfselect)), index=vdfselect.index)
    criteria = ['NPM%','ROE%','PE/ROE']
    #time_period = ['1yReturn','6mReturn','3mReturn','1mReturn']

    for row in vdfselect.index:
        for criterion in criteria:
            vdfselect.at[row,f"{criterion}_percentile"] = float(stats.percentileofscore(vdfselect[f"{criterion}"],vdfselect.at[row,f"{criterion}"]))

            
    for row in vdfselect.index:
        l = []
        for criterion in criteria:
            l.append(vdfselect.at[row,f"{criterion}_percentile"])
        avg = mean(l)
        #print(avg)
        vdfselect.at[row,"HQV_Score"] = avg
    vdfselect.to_csv("Nifty_Value.csv")
    vdfselect2 = vdfselect.sort_values("HQV_Score",ascending=False,ignore_index=True)[:15]
    vdfselect2.to_csv("NiftyValue15.csv")
 
    return vdfselect2

def get_rs_df():
    index_name = '^NSEI' # S&P 500
    returns_multiples = []

    # Index Returns
    index_df = pd.read_csv(path+'^NSEI.csv') 
    #pdr.get_data_yahoo(index_name, start_date, end_date)
    index_df['Percent Change'] = index_df['Adj Close'].pct_change()
    index_return = (index_df['Percent Change'] + 1).cumprod()[-1:].values[0]
    prices =[]
    # Find top 30% performing stocks (relative to the S&P 500)
    for ticker in tickers:
        # Download historical data as CSV for each stock (makes the process faster)
        df = pd.read_csv(path+ticker+'.csv')

        # Calculating returns relative to the market (returns multiple)
        df['Percent Change'] = df['Adj Close'].pct_change()
        stock_return = (df['Percent Change'] + 1).cumprod()[-1:].values[0]
    
        returns_multiple = round((stock_return / index_return), 2)
        returns_multiples.extend([returns_multiple])
        
        #print (f'r: {ticker}; Returns Multiple against Nifty 200: {returns_multiple}\n')
        #time.sleep(1)
        #stock_data[ticker]=df
    # Creating dataframe of only top 30%
    #data_sets = pd.DataFrame(stock_data)
    rs_df = pd.DataFrame(list(zip(tickers, returns_multiples)), columns=['Ticker', 'Returns_multiple'])
    rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True) * 100
    rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(.70)]

    # Checking Minervini conditions of top 30% of stocks in given list
    #rs_stocks = rs_df['Ticker']
    return rs_df
def get_export_list(rs_df):
    rs_stocks = rs_df['Ticker']
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "Price", "52wkHigh Gap%", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])

    for stock in rs_stocks:    
        try:
            #ticker = path + stock
            df = pd.read_csv(f'{path+stock}.csv', index_col=0)
            sma = [50, 150, 200]
            for x in sma:
                df["SMA_"+str(x)] = round(df['Adj Close'].rolling(window=x).mean(), 2)
            
            # Storing required values 
            currentClose = df["Adj Close"][-1]
            moving_average_50 = df["SMA_50"][-1]
            moving_average_150 = df["SMA_150"][-1]
            moving_average_200 = df["SMA_200"][-1]
            low_of_52week = round(min(df["Low"][-260:]), 2)
            high_of_52week = round(max(df["High"][-260:]), 2)
            gap_52wkHigh = round((high_of_52week - currentClose) / currentClose * 100,2)
            RS_Rating = round(rs_df[rs_df['Ticker']==stock].RS_Rating.tolist()[0])
            
            try:
                moving_average_200_20 = df["SMA_200"][-20]
            except Exception:
                moving_average_200_20 = 0

            # Condition 1: Current Price > 150 SMA and > 200 SMA
            condition_1 = currentClose > moving_average_150 > moving_average_200
            
            # Condition 2: 150 SMA and > 200 SMA
            condition_2 = moving_average_150 > moving_average_200

            # Condition 3: 200 SMA trending up for at least 1 month
            condition_3 = moving_average_200 > moving_average_200_20
            
            # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
            condition_4 = moving_average_50 > moving_average_150 > moving_average_200
            
            # Condition 5: Current Price > 50 SMA
            condition_5 = currentClose > moving_average_50
            
            # Condition 6: Current Price is at least 30% above 52 week low
            condition_6 = currentClose >= (1.3*low_of_52week)
            
            # Condition 7: Current Price is within 25% of 52 week high
            condition_7 = currentClose >= (.75*high_of_52week)
            
            # If all conditions above are true, add stock to exportList
            if(condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7):
                exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating ,"Price":currentClose, "52wkHigh Gap%" :gap_52wkHigh ,"50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 week High": high_of_52week}, ignore_index=True)
                #print (stock + " made the Minervini requirements")
        except Exception as e:
            #print (e)
            print(f"Could not gather data on {stock}")
            continue

    exportList = exportList.sort_values(by='RS_Rating', ascending=False)
    #print('\n', exportList)
    exportList.to_csv("Nse 200 Momentum.csv")

    return exportList

st.subheader('Stock Selection Analysis: Nifty 200 index stocks')

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Returns', 'Fundamental', 'Momentum','Charts','Data Update'])
    
#genre = st.sidebar.radio(
#     "Select Analysis tables",
#   ('Returns', 'Fundamental', 'Momentum','Charts','Data Update'))
    
with tab1:
#if genre == 'Returns':
    data = returns()
    sorted_data = sorted_returns(data)

    st.write("Sorted and  Ranked Top 15 on the basis of Returns")
    st.write(sorted_data)
    st.write('Momentum of returns. Full list')

    st.write(data)

with tab2:
#if genre == 'Fundamental':
    fdf = pd.read_csv('Nifty 200 funda data.csv')
    vdf = get_fundas(fdf)
    ranked_data = ranked_fundas(vdf)
    st.write('Sorted and Ranked based on fundas top 15')
    st.write(ranked_data)
    st.write('Ranking based on fundamentals. Full list')
    st.write(vdf)

with tab3:
#if genre == 'Charts':
    st.subheader('Stock charts app')

    st.subheader('Select Stock')
    add_selectbox = st.selectbox(
        "Select the stock for  chart or type in a few of letters of symbol.",
        nifty_data['Symbol']
    )

    if add_selectbox:
        symbol = add_selectbox
        company = nifty_data[nifty_data['Symbol']==symbol]['Company Name']
        company=company.values[0]
        #company = company['Company Name']
        st.write("You have selected: ", symbol)
        st.write(company)

        df = pd.read_csv('yearly/{}'.format(symbol)+'.csv')[-300:]

        st.header  = add_selectbox + '  Close \n'
        #st.line_chart(df['Close'])
        figc = chart(df)
        st.plotly_chart(figc, use_container_width=True)
        figc2 = chart2(df)
        st.plotly_chart(figc2, use_container_width=True)


with tab4:

#if genre == 'Momentum':

    st.write("High Momentum stocks")
    rs_df = get_rs_df()
    export_list = get_export_list(rs_df)
    st.write(export_list)

    #st.write("You didn't select comedy.")
    st.write("Relative Strength stocks top 30%")
    st.write(rs_df)
#st.write("You have selected: " + add_selectbox)


with tab5:

#if genre == 'Data Update':
    st.write("Database of stocks last updated on: ", last_update)

    if latest>last_update:

        x=snapshot()
        x= "Data Updated"
        st.write(x)
    else:
        st.write("UpDate is current. ", last_update)

    if st.button("Update database"):  

        st.warning('Warning. Page visits external sites to update data. Please wait. It may take sometime.')

        #get_funda_data()
        if latest>last_update:

            x=snapshot()
            x= "Data Updated"
            st.write(x)
        else:
            st.write("UpDate is current. ", last_update)



#st.write("Candlestick Pattern Observed table1:")
#st.write(cpattern)
#st.add_selectbox.selected
st.write('Great! \n')


