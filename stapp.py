import streamlit as st
import marketanalysis
import altair as alt

st.title(r"Nick Carroll's Efficient Frontier App")

stocks = st.text_input(
    "Please input the stock tickers of the portfolio that you are looking to optimize:",
    "AMZN AAPL MSFT",
).split(" ")

try:
    analysis = marketanalysis.portfolioAnalysis(stocks)
    top15 = marketanalysis.efficientFrontier(analysis)

    st.subheader(
        f"The efficient frontier for the chosen stocks ({stocks}) is plotted below:"
    )

    plot = (
        alt.Chart(analysis)
        .mark_point()
        .encode(x=alt.X("Expected Risk", scale=alt.Scale(zero=False)), y="Average Return")
        .interactive()
    )

    plotTop = (
        alt.Chart(top15)
        .mark_point()
        .encode(
            x=alt.X("Expected Risk", scale=alt.Scale(zero=False)),
            y="Average Return",
            color=alt.value("red"),
        )
    )


    st.altair_chart(plot + plotTop, use_container_width=True)

    st.subheader(
        f"The 15 portfolios with the best risk/reward ratio (as shown in red above) for the selected stocks ({stocks}) are:"
    )
    st.table(top15)
except:
    st.text("At least two tickers from the dataset must be included for this analysis.  Please read the text below regarding where the data comes from if there is any confusion as to why the tickers are not available.")

st.text(
    "This application uses the data from Kaggle dataset https://www.kaggle.com/datasets/paultimothymooney/stock-market-data.  There are 3,480 stock tickers that this application has information about from this dataset.  Many mutual funds and microcap stocks are not included in the available data.  This analysis ignores any tickers that aren't located in this data."
)
