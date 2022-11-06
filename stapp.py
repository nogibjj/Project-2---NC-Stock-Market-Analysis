import streamlit as st
import subprocess
import marketanalysis
import altair as alt

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

analysis = marketanalysis.portfolioAnalysis(stocks)

st.subheader(f"The efficient frontier for the chosen stocks ({stocks}) is plotted below:")

plot = alt.Chart(analysis).mark_circle().encode(
    x='Expected Risk', y='Average Return')

st.altair_chart(plot, use_container_width=True)

st.subheader(f"The top 15 portfolios for these stock tickers ({stocks}) are:")
st.table(marketanalysis.efficientFrontier(analysis))
