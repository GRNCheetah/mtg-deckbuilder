import requests
import json
from pathlib import Path

BASE_URL = 'http://api.magicthegathering.io/v1/cards?'


#def printCardInfo():
    

def downloadImg(deck_name, dict):
    json_obj = dict.json()
    if ("imageUrl" in json_obj["cards"][0]):
        img_url = json_obj["cards"][0]["imageUrl"]
        card_name = json_obj["cards"][0]["name"]
        print("[+]" + card_name)
        print("[+]Img found, downloading...")
        
        r = requests.get(img_url)
        if r.status_code == 200:
            with open(card_name + ".png", "wb") as f:
                f.write(r.content)
        else:
            print("[-]Image download failed")
    else:
        print("[-]No image to download")

def addCard(dict, csv_f):
    json_obj = dict.json()
    type = json_obj["cards"][0]["type"]
    name = json_obj["cards"][0]["name"]
    name = '"' + name + '"'
    print(name)
    colors = json_obj["cards"][0]["colorIdentity"]
    cmc = json_obj["cards"][0]["cmc"]
    
    
    if "creature" in type.lower():
        power = json_obj["cards"][0]["power"]
        toughness = json_obj["cards"][0]["toughness"]
        text = json_obj["cards"][0]["text"]
        text = '"' + text + '"'
        csv_f.write(name + "," + " ".join(colors) + "," + str(cmc) + "," + type + "," + str(power) + "," + str(toughness) + "," + text + ",,\n")
    elif "planeswalker" in type.lower():
        csv_f.write(name + "," + " ".join(colors) + "," + str(cmc) + "," + type + ",,,,,\n")
    else:
        text = json_obj["cards"][0]["text"]
        text = '"' + text + '"'
        csv_f.write(name + "," + " ".join(colors) + "," + str(cmc) + "," + type + ",,," + text + ",,\n")
    
    
    
   
'''
Will get the card information and add it to the spreadsheet
Overwrites the current spreadsheet atm
Also saves a copy of the picture of the card

'''
## Gets passed a str: deck name, str: card name, and a file: csv_f
def getInfo(deck_name, card_name, csv_f):
    # get the cards dictionary
    req = requests.get(BASE_URL + "name=" + card_name)
    
    # if the connection was good
    if (req.status_code == 200) and (int(req.headers["Count"]) >= 1):
        addCard(req, csv_f)
        downloadImg(deck_name, req)
    elif int(req.headers["Count"]) < 1:
        print("[-]No cards found with that name.")
    elif req.status_code == 403:
        print("[-]Exceeded the rate limit, wait a minute or so")
        print("[-]May have to wait up to an hour")
    elif req.status_code == 500:
        print("[-]Server problem, try again in a minute")
        print("[-]Status Code: " + str(req.status_code))
    elif req.status_code == 503:
        print("[-]Server is down for maintenance")
        print("[-]Status Code: " + str(req.status_code))
    else:
        print("[-]Connection failed")
        print("[-]Status Code: " + str(req.status_code))
    
## Start Message
def startMsg():
    print("\n\n  Welcome to the deck builder")
    print("To use, you will enter the name of your card. It will add it's")
    print("information to a spreadsheet for you to look at it. Currently,")
    print("if the name of the file you enter is already there, the deck will")
    print("be overwritten. Have fun!")

    
## Main Loop
def mainLoop():
    startMsg()
    print("\nEnter each card one at a time")    
    print("Type donezo when you are donezo")
    
    deck_name = input(">>What is the name of this deck? ")
    
    with open(deck_name + ".csv","w") as csv_f:
        csv_f.write("\"" + deck_name + "\",,,,,,,\n,,,,,,,\n")
        csv_f.write("Name,Colors,Mana Cost,Type,P,T,Text,,\n")
        card_name = input(">>Card name:")
            
        while card_name != "donezo":
            getInfo(deck_name, card_name, csv_f)
            card_name = input(">>Next card: ")
            
        csv_f.write(",,,,,,,")
        
        
## Hopefully this makes it easier
## The program will be represented by an object, the deck
## The deck has attributes, like it's name, where it's stored,
## how many cards it has, etc. Then the functions will add to or
## remove from the deck.
        
class MTGDeck:



        
mainLoop()


##     our_card_from_the_site_._json["cards"][use_this_to_choose_different_cards_returned]["identifier"]
#print(json_obj["cards"][0]["imageUrl"])
