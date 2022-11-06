#!/usr/bin/env bash

# A simple command line interface for the market analysis package

case $1 in 
    
    # Show the help message
    -h | --help)
    echo "Usage: cli.sh [option] [stock] [stock] [stock] [stock] [stock]"
    echo "Options:"
    echo "  -h, --help: Show this help message"
    echo "  download_data: Download the data from Kaggle"
    echo "  createdb: Create a database on AWS (include database name)"
    echo "  create_pathlist: Use this after downloading Kaggle data for the first time so the database knows where to find the data"
    echo "  update_tables: Update stock performance tables on AWS database"
    echo "  analysis: Run the analysis on the data (connect to AWS database for data)"
    echo "  analysis_fromcsv: Run the analysis on the data (local csv data downloaded from Kaggle)"
    ;;
    
    # Download the data from Kaggle
    "download_data")
    echo "Downloading data"
    kaggle datasets download -p datasets --unzip paultimothymooney/stock-market-data
    ;;

    # Find the best portfolios
    "analysis")
    echo "Running analysis"
    args=($@)
    # Run the analysis for each of the stocks
    python -c 'import marketanalysis; import sys; print(marketanalysis.efficientFrontier(marketanalysis.portfolioAnalysis(sys.argv[1:])))' ${args[@]:1:$#}
    ;;
    
    # Find the best portfolios
    "analysis_fromcsv")
    echo "Running analysis"
    # Find the paths to each of the stocks
    args=($@)
    declare -a file=()
    for stocks in ${args[@]:1:$#}
    do
        file+=($(find . -name $stocks.csv | head -1))
    done
    # Run the analysis for each of the stocks
    python -c 'import marketanalysis; import sys; print(marketanalysis.efficientFrontier(marketanalysis.portfolioAnalysis(sys.argv[1:])))' ${file[@]}
    ;;

    # Create a database in AWS
    "createdb")
    echo "Creating Database"
    python -c 'import createdb; import sys; createdb.createdb(sys.argv[1:])' $2 $AWS_STOCKDB_USERNAME $AWS_STOCKDB_PASSWORD $AWS_STOCKDB_HOSTNAME $AWS_STOCKDB_PORT
    echo "Database Created"
    ;;

    # Update tables to database in AWS
    "update_tables")
    echo "Updating Tables"
    python -c 'import createdb; import sys; createdb.updateTables(["stock_performance"] + sys.argv[1:])' $AWS_STOCKDB_USERNAME $AWS_STOCKDB_PASSWORD $AWS_STOCKDB_HOSTNAME $AWS_STOCKDB_PORT
    echo "Tables Updated"
    ;;

    # Update tables to database in AWS
    "create_pathlist")
    echo "Creating Path List"
    python -c 'import createdb; import sys; createdb.pathList()'
    echo "Creating Path List"
    ;;

esac
