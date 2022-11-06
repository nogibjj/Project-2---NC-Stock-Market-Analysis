# Project-3---NC-Stock-Market-Analysis
This project creates a Streamlit Application for plotting the efficient frontier of a selected group of stocks.  Please visit the application here:
https://nick-carroll1-project-2---nc-stock-market-analysis-stapp-2mmroj.streamlit.app/

This is a screenshot of what the application looks like:
![Project 3 Screenshot](https://user-images.githubusercontent.com/112578073/200200264-0459f850-aa90-43c1-9e6c-f1cc0e61fcd0.png)

Analysis of Stock Market data for project 3.

This project analyzes the efficient frontier of a stock portfolio.  It uses a Streamlit Application to allow users to input stock tickers and view a plot of the efficient frontier along with a table of the top 15 recommended portfolios.  The code for the Streamlit Application is in stapp.py.  

It also uses a command line tool (marketanalysis.sh) to download an updated version of the Kaggle dataset (https://www.kaggle.com/datasets/paultimothymooney/stock-market-data), create a database on AWS, update database tables on AWS, and analyze the data to find the efficient frontier for a portfolio of selected stocks.  Run ./marketanalysis.sh -h for help in using the features of the command line tool.

In order to download the Kaggle dataset, a user needs to include the user's Kaggle credentials or use a Kaggle token to gain access prior to downloading the data.  Downloading new data is not required to run the application, as the data is already in the AWS database, but it is required to updated the database with new data.  In order to gain access to the AWS database, a user needs to include their username and password, along with the hostname and port in their secrets and call these environment variables AWS_STOCKDB_USERNAME, AWS_STOCKDB_PASSWORD, AWS_STOCKDB_HOSTNAME, and AWS_STOCKDB_PORT respectively.

The application finds the efficient frontier of the selected stocks by making 500 randomized portfolios and plotting the risk and reward of each.  It plots all 500 randomized portfolios in blue, and plots the top 15 with the best risk to reward ratio in red.  It also displays a table of those top 15 with their average daily return, expected daily risk, portfolio make-up, and risk return ratio.  With the top 15 portfolios, a user can select the portfolio they deem best for themselves based upon their own risk appetite.  

*Please note that I created an issue tracking item because the tooltip functionality for the altair plot is not working with the Streamlit Application.  The tooltip works fine in a Jupyter notebook, but the Streamlit Application does not currently allow a user to hover over a datapoint in the plot and review its credentials.  There seems to be a conflict in the Streamlit environment that differs from the Jupyter notebook environment.  Please provide a resolution if available.*

This application has evolved since Project 2 began and has several scripts and code blocks providing functionality that is not related to the Streamlit Application.  It was originally set-up to use a FastAPI web application (using main.py), which is still functional, but the functionality of the Streamlit Application has exceeded the FastAPI functionality.  Additionally, there is a Dockerfile that allows the program to be containerized and deployed, but this also has been superceded by the Streamlit Application.  Furthermore, there is functionality to analyze the data from the downloaded csv files and to convert those files into a local sqlite database.  This funcionality can be expanded if there are benefits to continue with this functionality.
