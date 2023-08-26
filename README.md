# stock_market_Live_streaming_zerodha_kite_connect_api_trading

This repo queries the zerodha kite_connect api for obtaining live option oi and calculating the put call ratios and uploads them onto our own mysql server. 

-Start with the file that creates the daily trading symbol; It takes the latest daily fno bhavcopy csv from nse as an input and creates trading symbols from it. 
-Once the trading symbols are created and stored in the file named 'latest_intruments1.csv', run the LIVE_PCR_CALCULATIONS file. 
-In this file remember to put your api_key.txt as always and your zerodha user id. This file queries the api for every stock and finds its call open interest, put open interest, calculates the put call ratio 
and uploads all of them to individual stock tables in the MySQL database. This file will keep running throughout the day while the stock market functions. 
- The put call ratio is plotted in the nfo_live_pcr_plot file for any stock that the user is inputting and the plot periodically get updated.

- ENJOY TRADING USING PCR!
