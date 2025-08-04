from ib_insync import *

# Connect to TWS (devault TWS paper trading port is 7497)

ib = IB()
ib.connect('127.0.0.1', 7497, clientId = 1)

print('Connected:', ib.isConnected())

ib.disconnect()