import sqlite3
import pandas as pd
import os
import subprocess
import mysql.connector
from sqlalchemy import create_engine


# Create a database and table to store the stock performance information
def createSQLitedb():
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


def createdb(database, username, passwd, hostname, portnum):
    connection = mysql.connector.connect(
        user=username, password=passwd, host=hostname, port=portnum
    )
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)
        pass
    connection.close()


# Create a table to store the stock performance information
def updateTables(dbname, username, passwd, hostname, portnum):
    engine = create_engine(f"mysql://{username}:{passwd}@{hostname}:{portnum}/{dbname}")
    connection = engine.connect()
    stockPaths = pd.read_csv("datasets/stockPaths.csv", header=0, nrows=1)
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
            print(stockData.head())
            stockData.to_sql(
                f"{stock}_performance", connection, if_exists="replace", index=False
            )
            pass
        except:
            print(f"Error: {stock} not added to database")
            continue
        pass


# Select the first ten rows of the table for a given stock for testing purposes
def selectData(stock, dbname, username, passwd, hostname, portnum):
    connection = mysql.connector.connect(
        user=username, password=passwd, host=hostname, port=portnum, database=dbname
    )
    cursor = connection.cursor()
    select_query = f"SELECT * FROM {stock}_performance LIMIT 10;"
    cursor.execute(select_query)
    for eachRow in cursor:
        print(eachRow)
    connection.close()


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
    myuser = os.getenv("AWS_STOCKDB_USERNAME")
    mypassword = os.getenv("AWS_STOCKDB_PASSWORD")
    myhost = os.getenv("AWS_STOCKDB_HOSTNAME")
    myport = os.getenv("AWS_STOCKDB_PORT")
    database = "stock_performance"
    pathList()
    createdb(database, myuser, mypassword, myhost, myport)
    updateTables(database, myuser, mypassword, myhost, myport)
    # Select the first stock in the list for testing
    stock = (
        str(pd.read_csv("datasets/stockPaths.csv", header=0, nrows=1).loc[0])
        .split("/")[-1]
        .split(".")[0]
    )
    selectData(stock, database, myuser, mypassword, myhost, myport)
