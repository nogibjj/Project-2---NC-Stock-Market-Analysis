# Project-2---NC-Stock-Market-Analysis
Analysis of Stock Market data for project 2.

This project analyzes the efficient frontier of a stock portfolio.  It uses a command line tool (marketanalysis.sh) to download a Kaggle dataset (https://www.kaggle.com/datasets/paultimothymooney/stock-market-data) and analyze the data to find the efficient frontier for a portfolio of selected stocks.  It also uses FastAPI to create a web application to find the best portfolio of selected stocks from a web browser.  The program finds the efficient frontier by making 500 randomized portfolios of the selected stocks and returns the top 15 with the best risk to reward ratio.  With the top 15 portfolios, a user can select the portfolio they deem best for themselves based upon their own risk appetite.  The web application returns a JSON object from the dataframe of the best portfolios, showing the portfolio make-up, daily expected risk, daily average return, and risk to return ratio. 

![image](https://user-images.githubusercontent.com/112578073/194731772-6c6bb818-8283-46b6-ad99-4ebecbf5054b.png)

