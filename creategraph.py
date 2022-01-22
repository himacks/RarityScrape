import requests
import matplotlib.pyplot as plt
import numpy as np

collection = input("Collection: ")

URL = 'https://api-mainnet.magiceden.io/rpc/getGlobalActivitiesByQuery?q={"$match":{"collection_symbol":"' + collection + '"},"$sort":{"blockTime":-1,"createdAt":-1},"$skip":0}'

  


# location given here
  
# defining a params dict for the parameters to be sent to the API
PARAMS = {}
  
# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)
  
# extracting data in json format
data = r.json()

print(data)

xPlot = []
yPlot = []

startTime = 0

for transaction in data["results"]:
    if(transaction["txType"] == "initializeEscrow"):

        if (startTime == 0):
            startTime = transaction["blockTime"]


        timeOfSale = startTime - transaction["blockTime"]
        saleAmount = transaction["parsedList"]["amount"] / 1000000000

        xPlot.append(timeOfSale)
        yPlot.append(saleAmount)

        print("Sale: " + str(saleAmount))
        print("Time: " + str(timeOfSale))
        print("Transaction ID: " + str(transaction["transaction_id"]))
        print("Title: " + transaction["mintObject"]["title"])
        print("Mint Address: " + transaction["mintObject"]["mintAddress"])
        print()

x = np.array(xPlot)
y = np.array(yPlot)

plt.plot(x, y)
plt.show()