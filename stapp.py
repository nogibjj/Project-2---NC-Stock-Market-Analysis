import streamlit as st

st.title(r"Nick Carroll's Efficient Frontier App")

stocks = st.text_input('Please input the stock tickers of the portfolio that you are looking to optimize:', 'AMZN AAPL MSFT')

st.subheader(stocks)