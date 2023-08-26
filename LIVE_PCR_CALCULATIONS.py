import pandas as pd
import csv
import mysql
import mysql.connector
from kiteconnect import KiteConnect
import time
import re
import requests
from sqlalchemy import create_engine



#Login and accessing API

api_key = open('api_key.txt','r').read()
access_token = open('access_token.txt','r').read()

current_expiry = "22MAYFUT"
exchange = "NFO"


try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass






kite = KiteConnect(api_key = api_key)
engine = create_engine('xxxx_your_engine_details')
connection = engine.raw_connection()
db = connection.cursor()

kite.set_access_token(access_token)

user_id = "XX1234"   #enter your zerodha id




df = pd.read_csv("latest_instruments1.csv")

#breaking down trading symbols to seperate lists 

#condition df['segment']
df1 = df[(df['INSTRUMENT'] == "FUTSTK")]
names_list = df1["SYMBOL"].tolist()
s = set(names_list)
stocknames = list(s)
stocknames.sort()



print(len(stocknames))


with engine.connect() as conn, conn.begin():
    time.sleep(1)

#iterating throught the all the stocks and obtaining their call oi, put oi and put/call ratio

    while True:
    
        for name in stocknames:
            print(name)
            fut_tokens = []
            opt_ce_tokens  = []
            opt_pe_tokens = []
                
            current_fut_tokens = "{}:{}{}".format(exchange,name,current_expiry)
        
        
            df1 = df[(df['INSTRUMENT'] == "FUTSTK") & (df["SYMBOL"] == name)]
            ce = df[(df['INSTRUMENT'] == "OPTSTK") & (df["SYMBOL"] == name) & (df["OPTION_TYP"] =="CE")]
            pe = df[(df['INSTRUMENT'] == "OPTSTK") & (df["SYMBOL"] == name) & (df["OPTION_TYP"] =="PE")]
            

#putting all futures trading symbols into a list 

            fut_tr_symbols = df1["futcode"].tolist()
            for value in fut_tr_symbols:
                val1 = "{}:{}".format(exchange,value)   
                fut_tokens.append(val1)
                
#putting all call option tokes into a list 

            oc1 = ce["optcode"].tolist()
            oc1_set = set(oc1)
            opt_ce_symbols = list(oc1_set)
            for value in opt_ce_symbols:
                val2 = "{}:{}".format(exchange,value)
                opt_ce_tokens.append(val2)
                
#putting all put options tokens into a list 
            op1 = pe["optcode"].tolist()
            op1_set = set(op1)
            opt_pe_symbols = list(op1_set)
                        
            for value in opt_pe_symbols:
                val3 = "{}:{}".format(exchange,value)
                opt_pe_tokens.append(val3)
            print("All tokens obtained")
            
#querying the live API for the above tokens 

            data = kite.quote(fut_tokens)
            data1 = kite.quote(opt_pe_tokens)
            data2 = kite.quote(opt_ce_tokens)
            
#putting the data obtained  in dataframes 

            df2 = pd.DataFrame(data)
            df3 = pd.DataFrame(data1)
            df4 = pd.DataFrame(data2)
#calculating totals 

            total_fut_oi = df2.loc['oi'].sum()
            total_pe_oi = df3.loc['oi'].sum()
            total_ce_oi = df4.loc['oi'].sum()
            
#calculating put/call ratio 

            pcr = total_pe_oi/total_ce_oi

#uploading live data and calculations to mysql database 

            stockname2 = re.sub('[^a-zA-Z0-9 \n\.]', '', name)
            tablename = "{}livepcr".format(stockname2)
            fut_ltp = df2.loc["last_price"]['{}'.format(current_fut_tokens)]
            last_traded_time = df2.loc["last_trade_time"]['{}'.format(current_fut_tokens)]
            underlyingkey = '{}:{}'.format('NSE',name)
            data4 = kite.ltp([underlyingkey])
            underlying = data4['{}'.format(underlyingkey)]['last_price']
            print(fut_ltp)
            print(last_traded_time)
            print(pcr)
            
            db.execute("CREATE TABLE IF NOT EXISTS {}(id INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,time DATETIME UNIQUE, stock TEXT, puts BIGINT, calls BIGINT, pcr FLOAT, underlying FLOAT, futsym TEXT,futprice FLOAT, allfutoi BIGINT)".format(tablename))

            db.execute("INSERT IGNORE INTO {}(stock, puts, calls, pcr, time, underlying, futsym, futprice, allfutoi) VALUES('{}',{} ,{},{},'{}',{},'{}',{},{})".format(tablename,name,total_pe_oi,total_ce_oi,pcr,last_traded_time,underlying,current_fut_tokens, fut_ltp,total_fut_oi))
 


