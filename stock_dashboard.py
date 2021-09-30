import streamlit as st 
import requests
import yfinance as yf 
import plotly.graph_objects as go 
import plotly.express as px 
import pandas as pd


symbol = st.text_input('Enter Ticker: ')

screen = st.sidebar.selectbox('View', ('Overview', 'Fundamentals'))
ticker = yf.Ticker(symbol)

spy = yf.Ticker('SPY')
spy_df = spy.history(period = '5y',interval='1d')
spy_df.reset_index(inplace = True)


# Get Percentage Return 
r = [0]
for i in range(1,len(spy_df)):
    val = (spy_df.Close[i] - spy_df.Close[0]) / spy_df.Close[0] *100
    r.append(val)
spy_df['Return'] = r 


df = ticker.history(period = '5y',interval='1d')
df.reset_index(inplace=True)
# Percentage return for Ticker 
r = [0]
for i in range(1,len(df)):
    val = (df.Close[i] - df.Close[0]) / df.Close[0] *100
    r.append(val)
df['Return'] = r 


new_df = pd.DataFrame(columns=['Date', 'SPY Return', f'{symbol} Return'])
new_df['Date'] = spy_df.Date
new_df['SPY Return'] = spy_df.Return
new_df[f'{symbol} Return'] = df.Return

# Changing font size 
st.markdown("""<style>.small-font {font-size:12px !important;}</style> """, unsafe_allow_html=True)


# Screens 
if symbol: 
    if screen == 'Overview': 
        left,right = st.columns([1,3])

        with left:
            st.header(f'{symbol.upper()}')
            if ticker.info['logo_url']:
                st.image(ticker.info['logo_url'])

        with right: 
            st.subheader('Company Description: ')
            summ = ticker.info['longBusinessSummary']

            with st.expander(f'Description: {summ[0:250]} ... Read more'):
                # st.write(f'{summ}')

                st.markdown(f'<p class="small-font"> {summ} !!</p>', unsafe_allow_html=True)

    
        st.subheader('5 Year Daily Chart: ')
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])])

        st.write(fig)

        st.subheader('Percent Return vs SP500')
        per_return = px.line(new_df, x='Date', y=new_df.columns)
        st.write(per_return)


    if screen == 'Fundamentals':
        st.header(f'{symbol.upper()} Fundamentals')
        choice = st.sidebar.selectbox('Quarterly or Yearly Financials',['Yearly','Quarterly'])

        left, right = st.columns(2)

        with left: 
            
            st.write('Market Cap:   ', ticker.info['marketCap'])
            
            try: 
                st.write('Trailing P/E: ', ticker.info['trailingPE'])
            except KeyError as e: 
                st.write('Trailing P/E: None ')
      
                
                
            st.write('Dividend Rate:', ticker.info['dividendRate'])
            st.write('Book Value:   ', ticker.info['bookValue'])

        with right: 
            st.write('Price to Sales: ',ticker.info['priceToSalesTrailing12Months'])
            st.write('Forward P/E: ',   ticker.info['forwardPE'])
            st.write('Dividend Yield: ',ticker.info['dividendYield'])
            st.write('Price to Book: ', ticker.info['priceToBook'])


        if choice == 'Yearly':
            y_earning_df = ticker.earnings.reset_index()
            y_rev = px.bar(data_frame=y_earning_df, x=y_earning_df.Year,y=y_earning_df.Revenue)
            y_earning = px.bar(data_frame=y_earning_df, x=y_earning_df.Year,y=y_earning_df.Earnings)
            
            st.write(y_earning)
            st.write(y_rev)


        if choice == 'Quarterly':
            q_earning_df = ticker.quarterly_earnings.reset_index()
            rev = px.bar(data_frame = q_earning_df, x=q_earning_df.Quarter, y=q_earning_df.Revenue)
            earning = px.bar(data_frame = q_earning_df, x=q_earning_df.Quarter, y=q_earning_df.Earnings)
        
            st.write(earning)
            st.write(rev)
    
    
    

    
