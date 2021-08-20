import time, datetime, sys, json
import yfinance as yf
import stonksclient

# date_string = "Thu, 25 Mar 2021 20:49:35 GMT"
TSFORMAT = "%a, %d %b %Y %H:%M:%S %Z"

SECONDS_PER_HOUR = 3600

MARKETOPEN = datetime.datetime.now().replace(hour=6, minute=30, second=0, microsecond=0)
MARKETCLOSE = datetime.datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)
EIGHT_HOURS = datetime.timedelta(hours=8)


def createNotification(symbol="AAPL", low=0.0, high=999999999.99):
	while True:
		ticker = yf.Ticker(symbol)
		now = datetime.datetime.now()
		price = 0.5 * (ticker.info['bid'] + ticker.info['ask'])
		ts = ticker.info['timestamp']

		timestamp = datetime.datetime.strptime(ts, TSFORMAT)
		tdiff = round((timestamp - now).seconds / SECONDS_PER_HOUR)
		utc_offset = datetime.timedelta(hours=tdiff)
		timestamp -= utc_offset
		timestamp = timestamp.strftime("%b %m %Y %I:%M %p")

		if timestamp < MARKETOPEN or timestamp > MARKETCLOSE:
			print("Market is currently closed. Notification was not created.")
			break

		stock = [timestamp, symbol, price, low]
		if price < low or price > high:
			stonksclient.send_email(stock)
			print(([timestamp, symbol, price, low]))
			print('Notification sent.')
			break
		
		for i in range(60):
			time.sleep(1)
			print(ts)
			
		

# stonks.py [TICKER] <low> <high>
if __name__ == '__main__':
	symbol = sys.argv[1].upper()
	try: yf.Ticker(symbol).info
	except:
		print("Could not find ticker:{}".format(symbol))
		exit(1)

	low = 0.0
	high = 999999999.99
	try: low = float(sys.argv[2])
	except: pass
	try: high = float(sys.argv[3])
	except: pass
	print("Ticker will be checked every minute.\nNotification will be sent when {} drops below ${:.2f} or rises above ${:.2f}".format(symbol, low, high))
	createNotification(symbol, low, high)
