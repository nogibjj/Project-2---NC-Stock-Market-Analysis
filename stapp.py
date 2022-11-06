import streamlit as st
import subprocess
import marketanalysis

st.title(r"Nick Carroll's Efficient Frontier App")


# def frontier(stocks):
#     # Run the script
#     stockList = stocks.split(" ")
#     files = []
#     for eachStock in stockList:
#         files.append(
#             subprocess.run(
#                 ["find", ".", "-name", f"{eachStock}.csv"],
#                 capture_output=True,
#                 check=True,
#             )
#             .stdout.decode()
#             .split("\n")[0]
#         )
#         pass
#     # Return the result
#     return efficientFrontier(portfolioAnalysis(files))


stocks = st.text_input(
    "Please input the stock tickers of the portfolio that you are looking to optimize:",
    "AMZN AAPL MSFT",
).split(' ')



st.subheader(f"The top 15 portfolios for these stock tickers ({stocks}) are:")

st.table(marketanalysis.efficientFrontier(marketanalysis.portfolioAnalysis(stocks)))
