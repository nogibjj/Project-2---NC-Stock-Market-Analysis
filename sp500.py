import pandas as pd
import sqlite3
from datasets import Dataset
import mysql.connector
from sqlalchemy import create_engine
import os

sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]

username = os.getenv("AWS_STOCKDB_USERNAME")
password = os.getenv("AWS_STOCKDB_PASSWORD")
hostname = os.getenv("AWS_STOCKDB_HOSTNAME")
port = os.getenv("AWS_STOCKDB_PORT")
database = "stock_performance"

engine = create_engine(f"mysql://{username}:{password}@{hostname}:{port}/{database}")
connection = engine.connect()

firstStock = sp500.loc[0, "Symbol"]
df = pd.read_sql(
    f"SELECT date, close AS {firstStock} FROM {firstStock}_performance",
    connection,
    index_col="Date",
    parse_dates={"Date": "%Y-%m-%d"},
)

for eachStock in sp500.loc[1:, "Symbol"]:
    try:
        df = df.merge(
            pd.read_sql(
                f"SELECT date, close AS {eachStock} FROM {eachStock}_performance",
                connection,
                index_col="Date",
                parse_dates={"Date": "%Y-%m-%d"},
            ),
            how="outer",
            on="Date",
        ).copy()
        pass
    except:
        print(f"Error: {eachStock} not added to dataset/ not found in database")
        continue

print(df.shape)
dataset = Dataset.from_pandas(df)
location = "nick-carroll1/sp500"
dataset.push_to_hub(location)
