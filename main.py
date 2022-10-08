from fastapi import FastAPI
import subprocess
from marketanalysis import efficientFrontier, portfolioAnalysis

app = FastAPI()

@app.get("/")
async def default():
    return {"message": "Welcome to my Efficient Frontier API"}

@app.get("/stocks/")
async def frontier(stocks: str):
    # Run the script
    stockList = stocks.split(' ')
    files = []
    for eachStock in stockList:
        files.append(subprocess.run(['find', '.', '-name', f'{eachStock}.csv'], capture_output=True).stdout.decode().split("\n")[0])
        pass
    # Return the result
    return efficientFrontier(portfolioAnalysis(files)).to_json()