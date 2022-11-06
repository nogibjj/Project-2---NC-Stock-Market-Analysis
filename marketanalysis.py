#!/usr/bin/env python
# Market Analysis Script

# Import the necessary packages
import random
import pandas as pd
import os
from sqlalchemy import create_engine

# Read in the data from csv files
# def stockData(stockList):
#     assert (
#         len(stockList) >= 2
#     ), f"Only 1 stock in the list. Please add more stocks to the list. Current stock list: {stockList}."
#     iteration = 0
#     for stocks in stockList:
#         match iteration:
#             case 0:
#                 stockDf = pd.read_csv(
#                     stocks,
#                     parse_dates=["Date"],
#                     infer_datetime_format=True,
#                     index_col="Date",
#                     dayfirst=True,
#                 )
#                 iteration = 1
#                 pass
#             case 1:
#                 stockDf[stocks.split("/")[-1].split(".")[0]] = pd.read_csv(
#                     stocks,
#                     parse_dates=["Date"],
#                     infer_datetime_format=True,
#                     index_col="Date",
#                     dayfirst=True,
#                 )["Close"]
#                 stockDf[stockList[0].split("/")[-1].split(".")[0]] = stockDf["Close"]
#                 stockDf = stockDf.loc[
#                     :,
#                     list(map(lambda x: x.split("/")[-1].split(".")[0], stockList[:2]))[
#                         :2
#                     ],
#                 ]
#                 iteration = 2
#                 pass
#             case 2:
#                 stockDf[stocks.split("/")[-1].split(".")[0]] = pd.read_csv(
#                     stocks,
#                     parse_dates=["Date"],
#                     infer_datetime_format=True,
#                     index_col="Date",
#                     dayfirst=True,
#                 )["Close"]
#                 pass
#         pass
#     return stockDf.dropna()


# Read in the data from sql database
def stockSQLdata(stockList):
    assert (
        len(stockList) >= 2
    ), f"Only 1 stock in the list. Please add more stocks to the list. Current stock list: {stockList}."
    iteration = 0
    username = os.getenv("AWS_STOCKDB_USERNAME")
    password = os.getenv("AWS_STOCKDB_PASSWORD")
    hostname = os.getenv("AWS_STOCKDB_HOSTNAME")
    port = os.getenv("AWS_STOCKDB_PORT")
    database = "stock_performance"
    engine = create_engine(
        f"mysql://{username}:{password}@{hostname}:{port}/{database}"
    )
    connection = engine.connect()
    for stocks in stockList:
        if iteration == 0:
            try:
                stockDf = pd.read_sql(
                    f"SELECT date, close FROM {stocks}_performance;",
                    connection,
                    index_col="date",
                )
                stockDf = stockDf.rename(columns={"close": stocks})
                iteration = 1
                pass
            except:
                continue
        else:
            try:
                stockDf = stockDf.merge(
                    pd.read_sql(
                        f"SELECT date, close FROM {stocks}_performance;",
                        connection,
                        index_col="date",
                    ),
                    how="outer",
                    on="date",
                )
                stockDf = stockDf.rename(columns={"close": stocks})
                pass
            except:
                continue
        pass
    return stockDf.dropna()


# Transform data to %Change returns
def pctChange(stockDf):
    for eachCol in stockDf:
        stockDf[eachCol] = stockDf[eachCol] / stockDf[eachCol].shift() - 1
        pass
    return stockDf.dropna()


# Define the scale data function:
def scaleData(data, portfolioProportions):
    # Scale the data
    scaledData = data.copy()
    for eachStock in scaledData:
        scaledData[eachStock] = data[eachStock] * portfolioProportions[eachStock]
        pass
    return scaledData


# Calculate the average return of the portfolio
def averageReturn(scaledData):
    return scaledData.sum(axis=1).mean()


# Calculate the risk of the portfolio
def expectedRisk(scaledData):
    return scaledData.sum(axis=1).std()


# Analyze the risk and return of 500 random portfolios in the stock list
def portfolioAnalysis(stockList, randomPortfolios=500):
    # Read in the data
    # data = pctChange(stockData(stockList))
    data = pctChange(stockSQLdata(stockList))
    # Make an empty list of empty dictionaries
    portfolioProportions = [{} for i in range(randomPortfolios)]
    averageReturns = []
    expectedRisks = []
    # Make 500 random portfolios from the stock list
    for portfolios in range(0, randomPortfolios):
        remainder = 1.0
        shuffledStocks = list(data.columns)
        random.shuffle(shuffledStocks)
        for eachStock in shuffledStocks[:-1]:
            proportion = round(random.uniform(0, remainder - 0.01), 2)
            portfolioProportions[portfolios][eachStock] = proportion
            remainder = remainder - proportion
            pass
        portfolioProportions[portfolios][shuffledStocks[-1]] = round(remainder, 2)
        pass
        # Scale the data based on the portfolio proportions
        scaledData = scaleData(data, portfolioProportions[portfolios])
        # Get average return and risk for each portfolio
        averageReturns.append(averageReturn(scaledData))
        expectedRisks.append(expectedRisk(scaledData))
        pass
    return pd.DataFrame(
        {
            "Average Return": averageReturns,
            "Expected Risk": expectedRisks,
            "Portfolio Make-up": portfolioProportions,
        }
    )


# Subset the portfolios near the efficient frontier
def efficientFrontier(portfolioDF):
    portfolioDF["Risk Return Ratio"] = (
        portfolioDF.loc[:, "Average Return"] / portfolioDF.loc[:, "Expected Risk"]
    )
    return portfolioDF.sort_values("Risk Return Ratio", ascending=False).head(15)


if __name__ == "__main__":
    stockList = ["AAPL", "AMZN", "MSFT"]
    print(efficientFrontier(portfolioAnalysis(stockList)))
