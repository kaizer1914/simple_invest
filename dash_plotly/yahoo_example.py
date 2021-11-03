import yfinance

# ticker = 'AQUA.ME'
# ticker = 'ISKJ.ME'
ticker = 'GCHE.ME'
data = yfinance.Ticker(ticker)

info = data.info

# get historical market data
hist = data.history(period="max")

# show actions (dividends, splits)
actions = data.actions

# show dividends
dividends = data.dividends

# show splits
splits = data.splits

# show financials
financials = data.financials
quarterly_financials = data.quarterly_financials

# show major holders
major_holders = data.major_holders

# show institutional holders
institutional_holders = data.institutional_holders

# show balance sheet
balance_sheet = data.balance_sheet
quarterly_balance_sheet = data.quarterly_balance_sheet

# show cashflow
cashflow = data.cashflow
quarterly_cashflow = data.quarterly_cashflow

# show earnings
earnings = data.earnings
quarterly_earnings = data.quarterly_earnings

# show sustainability
sustainability = data.sustainability

# show analysts recommendations
recommendations = data.recommendations

# show next event (earnings, etc)
calendar = data.calendar

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
isin = data.isin

# show options expirations
options = data.options

# show news
news = data.news

# get option chain for specific expiration
# opt = data.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts


print(info)
