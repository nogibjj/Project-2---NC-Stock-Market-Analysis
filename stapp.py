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
).split(" ")

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

hover = alt.selection_single(
    fields=["Portfolio Make-up"],
    nearest=True,
    on="mouseover",
    empty="none",
)

tooltips = (
    alt.Chart(data)
    .mark_rule()
    .encode(
        x=alt.X("Expected Risk", scale=alt.Scale(zero=False)),
        y="Average Return",
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[alt.Tooltip("Portfolio Make-up", title="Portfolio Make-up")],
    )
    .add_selection(hover)
)

st.altair_chart(plot + plotTop + tooltips, use_container_width=True)

st.subheader(f"The top 15 portfolios for these stock tickers ({stocks}) are:")
st.table(top15)
