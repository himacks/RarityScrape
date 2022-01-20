
# importing the requests library
import requests
import collections
from collections import Counter
from matplotlib import pyplot as plt
import numpy as np

  


# api-endpoint

collection = input("Collection: ")



URL = 'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q={"$match":{"collectionSymbol":"' + collection + '"},"$sort":{"takerAmount":1,"createdAt":-1},"$skip":0}'
  
# location given here
  
# defining a params dict for the parameters to be sent to the API
PARAMS = {}
  
# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)
  
# extracting data in json format
data = r.json()


priceSum = 0
numListings = 0
lowestPrice = 0

nftDictionary = collections.defaultdict(list)

for listing in data["results"]:
    attributes = listing["attributes"]
    numListings += 1
    price = listing["price"]
        
    priceSum += price


    print(attributes)

    for attribute in attributes:

        try:
            trait = "trait_type"
            attribute[trait]
        except Exception as e:
            trait = "trait type"

        nftDictionary[attribute[trait]].append(attribute["value"])


    
print("------Aggregate Data------")
print("# of Listings: " + str(numListings))

for attribute in nftDictionary:
    print("Attribute: " + attribute)
    print("------------------------")
    nftDictionary[attribute] = {"Items": Counter(nftDictionary[attribute]), "Statistics": []}

    #print(nftDictionary[attribute])

    averageOccurance = 0
    characteristicCount = 0

    occuranceList = []

    for characteristic in nftDictionary[attribute]["Items"]:
        occuranceOfCharacteristic = nftDictionary[attribute]["Items"][characteristic]
        occuranceList.append(occuranceOfCharacteristic)
        averageOccurance += occuranceOfCharacteristic
        characteristicCount += 1

    averageOccurance = averageOccurance / characteristicCount

    median = max(occuranceList)
    highestSpread = 0
    print("Median: " + str(median))

    #print(averageOccurance)


    for characteristic in nftDictionary[attribute]["Items"]:
        occuranceOfCharacteristic = nftDictionary[attribute]["Items"][characteristic]

        spread = abs(median - occuranceOfCharacteristic)

        if(spread > highestSpread):
            highestSpread = spread


    if(spread != 0):
        highestSpread = median / spread
    else:
        highestSpread = 1.06

    for characteristic in nftDictionary[attribute]["Items"]:
        occuranceOfCharacteristic = nftDictionary[attribute]["Items"][characteristic]
        nftDictionary[attribute]["Items"][characteristic] = {}


        nftDictionary[attribute]["Items"][characteristic]["count"] = occuranceOfCharacteristic

        rarity = occuranceOfCharacteristic/numListings #number of items with this attribute divided by total number of items
        nftDictionary[attribute]["Items"][characteristic]["rarity"] = rarity

        deviationFromAverage = averageOccurance / occuranceOfCharacteristic
        nftDictionary[attribute]["Items"][characteristic]["deviationFromAverage"] = deviationFromAverage


        if(highestSpread > 1.05):
            deviationRarity = 1
        else:
            deviationRarity = rarity / deviationFromAverage

        nftDictionary[attribute]["Items"][characteristic]["deviationRarity"] = deviationRarity

            
        print(str(characteristic) + ": " + str(occuranceOfCharacteristic) + " | Rarity: " + str(rarity) + " | Deviation: " + str(deviationFromAverage) + " | DeviationRarity: " + str(deviationRarity))

        

    
#print(nftDictionary)

unsortedNFTList = []

if(True):
    for listing in data["results"]:
        title = listing["title"]
        price = listing["price"]
        mintAddress = listing["mintAddress"]
        attributes = listing["attributes"]
        masterRarity = 1
        lowestPrice = price

        #print("Title: " + str(title))
        #print("Price: " + str(price))
        #print("Mint Address: " + str(mintAddress))
        
        for attribute in attributes:
            try:
                trait = "trait_type"
                nftDictionary[attribute[trait]]
            except Exception as e:
                trait = "trait type"

            statisticalRarity = nftDictionary[attribute[trait]]["Items"][attribute["value"]]["rarity"]
            masterRarity *= statisticalRarity
            #print("Attribute: " + attribute["trait_type"] +  " | Value: " + attribute["value"] + " | Deviation Rarity: " + str(devRarity))
            #print(str(nftDictionary[attribute["trait_type"]]))
        #print("Combined Rarity: " + str(masterRarity * 10000000))

        unsortedNFTList.append({"name": title, "combRarity": masterRarity * 10000000, "price": price, "mintAddress": mintAddress})
    print()


sortedNFTList = sorted(unsortedNFTList, key=lambda d: d['combRarity'], reverse=True) 


ranking = numListings

priceRankingList = []

rankingList = []

i = 0

for listing in sortedNFTList:

    price = listing["price"]
    priceDeviation = price / priceSum

    print("Title: " + listing["name"])
    print("Combined Rarity: " + str(listing["combRarity"]))
    print("Price: " + str(price))
    print("Price Deviation: " + str(priceDeviation))


    if(priceDeviation < 1):
        priceRankingList.append(listing["price"])
        rankingList.append(i)
        i += 1

    print("Ranking: " + str(ranking) + "/" + str(numListings))

    ranking -= 1

    print("Link: https://magiceden.io/item-details/" + listing["mintAddress"])
    print()


x = np.array(rankingList)
y = np.array(priceRankingList)
m, b = np.polyfit(x, y, 1)

plt.plot(x, y, 'o')
plt.plot(x, m*x + b)


plt.show()
