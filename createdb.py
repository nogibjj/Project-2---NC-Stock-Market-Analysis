import sqlite3
import pandas as pd
import subprocess


# Create a database and table to store the stock performance information
def createdb():
    connection = sqlite3.connect("datasets/data.db")
    stockPaths = pd.read_csv("datasets/stockPaths.csv", header=0)
    for eachStock in stockPaths.index:
        try:
            stockPath = stockPaths.loc[eachStock][0]
            stock = stockPath.split("/")[-1].split(".")[0]
            stockData = pd.read_csv(
                stockPath,
                header=0,
                parse_dates=["Date"],
                infer_datetime_format=True,
                dayfirst=True,
            )
            stockData.to_sql(
                f"{stock}_performance", connection, if_exists="replace", index=False
            )
            pass
        except:
            print(f"Error: {stock} not added to database")
            continue


# Select the first ten rows of the table for a given stock for testing purposes
def selectData(stock):
    connection = sqlite3.connect("datasets/data.db")
    cursor = connection.cursor()
    select_query = f"SELECT * FROM {stock}_performance LIMIT 10"
    for eachRow in cursor.execute(select_query):
        print(eachRow)


# Create a list of file paths for each stock (selecting only unique stocks) and storing in csv
def pathList():
    pd.Series(
        pd.Series(
            subprocess.run(
                ["find", ".", "-name", "*.csv"],
                capture_output=True,
                check=True,
            )
            .stdout.decode()
            .split("\n")
        )
        .apply(lambda x: x.split("/")[-1].split(".")[0])
        .dropna()
        .unique()
    ).apply(
        lambda y: subprocess.run(
            ["find", ".", "-name", f"{y}.csv"],
            capture_output=True,
            check=True,
        )
        .stdout.decode()
        .split("\n")[0]
    ).to_csv(
        "datasets/stockPaths.csv", index=False
    )


if __name__ == "__main__":
    import time

    start = time.time()
    # pathList()
    # createdb()
    # Select the first stock in the list for testing
    stock = (
        str(pd.read_csv("datasets/stockPaths.csv", header=0, nrows=1).loc[0])
        .split("/")[-1]
        .split(".")[0]
    )
    selectData("TNC")
    print(f"Time taken: {time.time() - start}")
