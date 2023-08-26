import pandas as pd 
import re
from datetime import datetime

df = pd.read_csv("fo30SEP2022bhav.csv")
print(df.head())

#for futures 
month_key = []
month31 = ["JAN","MAR","MAY","JUL","AUG","OCT","DEC"]


df[['day','month','year']] = df.EXPIRY_DT.str.split("-",expand = True)
df["year"] = df["year"].apply(pd.to_numeric)
df["year"] = df["year"] -2000
df["month"] = df["month"].str.upper()
df['day'] = df['day'].str.pad(2, side ='left', fillchar ='0')
print(df.head())

df['ins'] = df["INSTRUMENT"].astype(str).str[0:3]
df['expiry2'] = pd.to_datetime(df["EXPIRY_DT"])
df['month2'] = df['expiry2'].dt.month
#df['month2'] = df['month'].astype(str).str[0]
df['we'] = df['year'].astype(str)+df['month2'].astype(str)+df['day']

df['futcode'] = df["SYMBOL"]+ df["year"].astype(str)+ df["month"]+df["ins"]
df['optcode'] = df["SYMBOL"] + df["year"].astype(str)+df['month']+df['STRIKE_PR'].astype(str).replace('\.0', '', regex=True)+df['OPTION_TYP']
df['woptcode'] = df['SYMBOL']+df['we']+df['STRIKE_PR'].astype(str).replace('\.0', '', regex=True)+df['OPTION_TYP']
df['foptcode'] = ""


for i,row in df.iterrows():
    if row['INSTRUMENT'] == "OPTIDX":
        if row['month'] in month31:
            print(row)
            if int(row['day']) < 25:
                df.at[i,'foptcode'] = row['woptcode']

            else:
                df.at[i,'foptcode'] = row['optcode']
        elif row['month'] == "FEB":
            if row['year'] % 4 ==0:
                if int(row['day'])< 23:
                    df.at[i,'foptcode'] = row['woptcode']
                else:
                    df.at[i,'foptcode'] = row['optcode']
            else:
                if int(row['day'])< 22:
                    df.at[i,'foptcode'] = row['woptcode']
                else:
                    df.at[i,'foptcode'] = row['optcode']                                             
        else:
            if int(row['day']) < 24:
                df.at[i,'foptcode'] = row['woptcode']
            else:
                df.at[i,'foptcode'] = row['optcode']
    else:
        df.at[i,'foptcode'] = row['optcode']
        

#Expiry adjustment 
# =============================================================================
# 
# a = pd.to_datetime('2022-06-30') 
# print(a)
# df = df[df["expiry2"]> a]
# 
# 
# 
# =============================================================================



print(df.head())
df.to_csv("latest_instruments1.csv")  
    


