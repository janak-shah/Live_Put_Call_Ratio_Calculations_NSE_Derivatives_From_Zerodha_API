import sys
sys.path.append(r"c:\users\rahul\appdata\roaming\python\python37\site-packages")
sys.path

import logging
from kiteconnect import KiteConnect


logging.basicConfig(level=logging.DEBUG)
api_key = open('api_key.txt','r').read()
api_secret = open('api_secret.txt','r').read()

kite = KiteConnect(api_key= api_key)


# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

#https://kite.zerodha.com/connect/login?api_key=7ep7j6u4h3vhfv8q
#Dollar@123 /668366



data = kite.generate_session("nPNdgMzxkl6N4Lqm82uq1vrdaGHqvXGd", api_secret= api_secret)
print(data)
kite.set_access_token(data["access_token"])
access_token = data['access_token']
print(access_token)
file1 = open("access_token.txt","w")
file1.write(access_token)




# =============================================================================
# # Place an order
# try:
#     order_id = kite.place_order(tradingsymbol="INFY",
#                                 exchange=kite.EXCHANGE_NSE,
#                                 transaction_type=kite.TRANSACTION_TYPE_BUY,
#                                 quantity=1,
#                                 order_type=kite.ORDER_TYPE_MARKET,
#                                 product=kite.PRODUCT_NRML)
# 
#     logging.info("Order placed. ID is: {}".format(order_id))
# except Exception as e:
#     logging.info("Order placement failed: {}".format(e.message))
# 
# # Fetch all orders
# kite.orders()
# 
# # Get instruments
# kite.instruments()
# 
# # Place an mutual fund order
# kite.place_mf_order(
#     tradingsymbol="INF090I01239",
#     transaction_type=kite.TRANSACTION_TYPE_BUY,
#     amount=5000,
#     tag="mytag"
# )
# 
# # Cancel a mutual fund order
# kite.cancel_mf_order(order_id="order_id")
# 
# # Get mutual fund instruments
# kite.mf_instruments()
# 
# =============================================================================
