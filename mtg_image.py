import requests
import json
from pathlib import Path
import os
       
## Start Message
def startMsg():
    print("\n--------------------------------")
    print("\n  Welcome to the deck builder")
    print("To use, you will enter the name of your card. It will add it's")
    print("information to a spreadsheet for you to look at it. The image will")
    print("also be saved. Have fun!")

        
## Hopefully this makes it easier
## The program will be represented by an object, the deck
## The deck has attributes, like it's name, where it's stored,
## how many cards it has, etc. Then the functions will add to or
## remove from the deck.
        
class MTGDeck:
    ## Url of the api
    BASE_URL = 'http://api.magicthegathering.io/v1/cards?'

    ## Get the name of the deck and add start a file connection
    def __init__(self):
        self.d_name = input("\n\nName of the deck: ")
        self.d_dir = os.getcwd() + "\\" + self.d_name
        if not(os.path.exists(self.d_dir)):
            os.makedirs(self.d_dir + "\\img" )
            self.d_file = open(self.d_dir + "\\" + self.d_name + ".csv","w+")
            self.d_file.write("\"" + self.d_name + "\",,,,,,,\n,,,,,,,\n")
            self.d_file.write("Name,Colors,Mana Cost,Type,P,T,Text,,\n")
        else:
            self.d_file = open(self.d_dir + "\\" + self.d_name + ".csv","a")
        
        
    ## Checks conn to server, returns true if conn was good, false if
    ## something was up. Will also output the error
    def checkConn(self, req):
        if (req.status_code == 200):
            return True
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

        return False
        
    def downloadImg(self, card_info):
        
        if ("imageUrl" in card_info):
            img_url = card_info["imageUrl"]
            card_name = card_info["name"]
            print("[+]Img found, downloading...")
            
            r = requests.get(img_url)
            if r.status_code == 200:
                with open(self.d_dir + "\\img\\" + card_name + ".png", "wb") as f:
                    f.write(r.content)
            else:
                print("[-]Image download failed")
        else:
            print("[-]No image to download")
        
    ## Prints some info on a card
    def printCardInfo(self, card_info):
        ## card_info is a dictionary
        print(card_info["name"] + "\t" + card_info["cmc"] + "\t" + card_info["type"])
        print(card_info["setName"])
        print(card_info["text"])
        
    def promptCards(self):
        user = ""
        print("\nEnter names of cards, leave blank to end")
        user = input("Card: ")
        while user != "":
            self.addCardToDeck(user)
            user = input("\nNext card (Blank to end): ")
        
        
    ## Choose the card
    def chooseCard(self, card_list, num_cards):
        user_choice = 0
        
        ## print the cards
        for x in range(num_cards):
            print("\n" + str(x+1) + ": " + card_list[x]["name"] + "\tMana: " + str(card_list[x]["cmc"]) + "  |  Type: " + card_list[x]["type"])
            print("Set Name: " + card_list[x]["setName"])
            print(card_list[x]["text"])
            
        ## get a choice
        user_choice = input("Choose a card: ")

        while not(int(user_choice) > 0 and int(user_choice) <= num_cards):
            user_choice = input("Error, try again: ")
            
        return int(user_choice) - 1
 
    ## The full func to add a card to the deck. All it needs it the name
    ## Add the card to the spreadsheet. Copy image of card to folder
    def addCardToDeck(self, card_name):
        ## Do request
        req = requests.get(self.BASE_URL + "name=" + card_name)
        ## Card list
        card_list = req.json()["cards"]
        num_cards = len(card_list)
        
        ## Make sure connection was fine
        if self.checkConn(req):
            if (num_cards < 1): ## Make sure there's at least one card to work with
                print("[-]No cards found with that name.")
            else:
                card_info = card_list[self.chooseCard(card_list,num_cards)]
                self.addCard(card_info)
                self.downloadImg(card_info)
                
                
    def addCard(self, card_info):
        
        ## Put all of the card info into vars
        name = card_info["name"]
        type = card_info["type"]
        colors = card_info["colorIdentity"]
        cmc = card_info["cmc"]
        
        ## Escape commas in the names
        name = '"' + name + '"'
        type = '"' + type + '"'
        
        
        ## Different cards have different bits of information
        if "creature" in type.lower():
            power = card_info["power"]
            toughness = card_info["toughness"]
            text = card_info["text"]
            
            text = '"' + text + '"'
            
            self.d_file.write(name + "," + " ".join(colors) + "," + str(cmc) + "," + type + "," + str(power) + "," + str(toughness) + "," + text + ",,\n")
        
        elif "planeswalker" in type.lower():
            self.d_file.write(name + "," + " ".join(colors) + "," + str(cmc) + "," + type + ",,,,,\n")
        
        else:
            text = card_info["text"]
            text = '"' + text + '"'
            
            self.d_file.write(name + "," + " ".join(colors) + "," + str(cmc) + "," + type + ",,," + text + ",,\n")
         
            
    ## Fix it up nice
    def closeDeck(self):
        self.d_file.close()
    

def main():

    startMsg()
    

    ## Initialize the deck
    deck = MTGDeck()
    
    ## Prompt for all cards
    deck.promptCards()
    
    ## Close out the deck
    deck.closeDeck()
        

if __name__ == '__main__':
    main()


