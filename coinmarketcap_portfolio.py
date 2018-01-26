#! python3
# coinmarketcap_portfolio.py - uses coinmarketcap api to update you alt-coin portfolio

import requests, copy, datetime
import pandas as pd


# grabbing our API
r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
x = r.json()

# making our DataFrame
df = pd.DataFrame(x)

# dropping columns we don't need
df = df.drop(['id', 'total_supply', 'price_btc', 'max_supply', 'available_supply'], axis=1)

# getting rid of NaN values by using notnull
df = df[df['market_cap_usd'].notnull()]

# convert objects into floats
df = df.apply(pd.to_numeric, errors='ignore')

# list of coins
btc = (df['name'] == 'Bitcoin')
eth = (df['name'] == 'Ethereum')

# making our portfolio
folio_raw = df[btc | eth]

# must make a deepcopy in order to multiply the column by amt_list
folio = copy.deepcopy(folio_raw)

# coin_variables
eth_amt = 1
btc_amt = 1

amt_list = [btc_amt, eth_amt]

# getting our portfolio in order for the multiplication
folio = folio.sort_values('symbol', ascending=True)

# adding an amount owned total (.values makes the keys match up)
folio['amt_owned'] = pd.Series(amt_list).values

# multiplying amt_list by price_usd in order to create a new column 'total'
folio['total'] = folio['price_usd'] * amt_list

# sum variables
eth_sum_var = (folio['name'] == 'Ethereum')
btc_sum_var = (folio['name'] == 'Bitcoin')

# adding a sum row
folio_sum = pd.DataFrame(data=folio[['total']].sum()).T

# add missing columns
folio_sum = folio_sum.reindex(columns=folio_sum.columns)

# append to our dataframe
folio = folio.append(folio_sum, ignore_index=True)

# replacing Nan values with empty strings
folio = folio.fillna("")

# rounding numbers in our dataframe
folio = folio.round(2)

# shows column headers
name_col = list(folio)

# insert name to front of the folio
name_col.insert(0, name_col.pop(name_col.index('name')))

# moving our amount owned column right before our total column
amt_owned_idx = (len(folio.columns) - 2)
amt_owned_col = name_col.pop(name_col.index('amt_owned'))
name_col.insert(amt_owned_idx, amt_owned_col)

# using ix to reorder
folio = folio.ix[:, name_col]

# running the portfolio
print(folio)
