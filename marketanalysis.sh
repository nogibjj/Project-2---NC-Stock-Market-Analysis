#!/usr/bin/env bash

# A simple command line interface for the market analysis package

case $1 in 
    -h | --help)
    echo "Usage: cli.sh [option] [stock] [stock] [stock] [stock] [stock]"
    echo "Options:"
    echo "  -h, --help: Show this help message"
    echo "  download_data: Download the data from Kaggle"
    echo "  analysis: Run the analysis on the data"
    ;;
    "download_data")
    echo "Downloading data"
    kaggle datasets download -p datasets --unzip paultimothymooney/stock-market-data
    ;;
    "analysis")
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
esac
