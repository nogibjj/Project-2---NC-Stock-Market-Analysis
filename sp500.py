import pandas as pd
import marketanalysis
import sqlite3
from datasets import Dataset

sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
connection = sqlite3.connect("datasets/data.db")

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
