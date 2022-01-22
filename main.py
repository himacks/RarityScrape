
# importing the requests library
from asyncio.windows_events import NULL
from os import stat
import requests
from colorama import init, Fore, Back, Style
from collections import Counter

init()


# api-endpoint

collection = input("Collection: ")

queryFinished = False

skip = 0
numListings = 0
floorPrice = 100000000000000
nftDictionary = {}
traitsShape = []
listingTemplate = {}
sortedNFTList = []

while(not queryFinished):

    URL = 'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q={"$match":{"collectionSymbol":"' + collection + '"},"$sort":{"takerAmount":1,"createdAt":-1},"$skip":' + str(skip) + '}'
    
    # location given here
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {}
    
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
    
    # extracting data in json format
    data = r.json()

    numListingsInThisQuery = 0

    for listing in data["results"]:

        numListings += 1
        numListingsInThisQuery += 1

        attributes = listing["attributes"]
        price = listing["price"]

        print("cataloged " + listing["title"])

        if(price < floorPrice and price > 0):
            floorPrice = price

        for attribute in attributes:

            try:
                trait = "trait_type"
                attribute[trait]
            except Exception as e:
                trait = "trait type"


            if (attribute[trait] not  in traitsShape):
                traitsShape.append(attribute[trait])
                listingTemplate[attribute[trait]] = {"null": 1}

            traitCount = 0

            if(attribute[trait] not in nftDictionary):
                nftDictionary[attribute[trait]] = {"Items": {}, "Total": 0}
                traitCount += 1
                
            if(attribute[trait] in nftDictionary and attribute["value"] not in nftDictionary[attribute[trait]]["Items"]):
                nftDictionary[attribute[trait]]["Items"][attribute["value"]] = 1
            else:
                nftDictionary[attribute[trait]]["Items"][attribute["value"]] += 1

            nftDictionary[attribute[trait]]["Total"] += traitCount


    for listing in data["results"]:
        price = listing["price"]
        priceFromFloor = price / floorPrice
        title = listing["title"]
        link = "https://magiceden.io/item-details/" + listing["mintAddress"]
        attributes = listing["attributes"]
        statRarity = 1
        listingShape = listingTemplate.copy()



        for attribute in attributes:
            if(attribute["trait_type"] in listingShape):
                #print(nftDictionary[attribute["trait_type"]])
                try:
                    rarity = nftDictionary[attribute["trait_type"]]["Items"][attribute["value"]] / numListings
                except KeyError as e:
                    rarity = 1
                    print(attribute["value"])
                    print(Fore.RED + "KeyError, setting Statistical Rarity to 1" + Style.RESET_ALL)
                listingShape[attribute["trait_type"]] = {attribute["value"]: rarity}
                statRarity *= rarity


        #for trait in traitsShape:
            #print("Trait Type: " + trait + " | Value: ")





        sortedNFTList.append({"title": title, "price": price, "link": link, "statRarity": statRarity, "priceFromFloor": priceFromFloor, "listingShape": listingShape})

        #print("---------------------------")
    
    if (numListingsInThisQuery < 500):
        queryFinished = True
    else:
        numListingsInThisQuery = 0
        skip += 500

sortedNFTList = sorted(sortedNFTList, key=lambda d: d['statRarity'], reverse=True) 

ranking = numListings

for listing in sortedNFTList:
    
    priceFromFloor = (listing["priceFromFloor"] - 1) * 100

    listingShape = listing["listingShape"]

    rarestPercentage = 1
    rarestAttribute = {}

    
    if(priceFromFloor < 5):
        color = Fore.CYAN
    elif (priceFromFloor < 10):
        color = Fore.BLUE
    elif (priceFromFloor < 20):
        color = Fore.MAGENTA
    elif (priceFromFloor < 40):
        color = Fore.YELLOW
    else:
        color = Fore.RED

    print("Title: " + Fore.WHITE + listing["title"] + Style.RESET_ALL)
    print("Price: " + color + str(listing["price"]) + " SOL" + Style.RESET_ALL)
    #print("Price from Floor: " + Fore.WHITE + str(priceFromFloor) + Style.RESET_ALL)
    print("Statistical Rarity: " + Fore.WHITE + str(listing["statRarity"]) + Style.RESET_ALL)
    print("Ranking: " + Fore.WHITE + str(ranking) + "/" + str(numListings) + Style.RESET_ALL)



    #print("--------Attributes--------")

    for attribute in listingShape.keys():

        attributePercentage = list(listingShape[attribute].values())[0]

        #print(attribute + ": " + Fore.WHITE + list(listingShape[attribute].keys())[0] + " - " + str(attributePercentage * 100) + "%" + Style.RESET_ALL)

        if(attributePercentage < rarestPercentage):
            rarestPercentage = attributePercentage
            rarestAttribute = listingShape[attribute]
            rarestAttribute["Attribute"] = attribute 

    #print()
    print("Rarest Attribute: " + Fore.WHITE + str(list(rarestAttribute.values())[1]) + " - Value: " + str(list(rarestAttribute.keys())[0]) + " | Rarity: " + Fore.YELLOW + str(list(rarestAttribute.values())[0] * 100) + "%" + Style.RESET_ALL)
    #print("--------------------------")
    print("Link: " + Fore.WHITE + listing["link"] + Style.RESET_ALL)
    print()
    print()

    ranking -= 1
