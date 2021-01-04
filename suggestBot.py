from __future__ import print_function
import os

import discord
import random
import json
import time

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


##potential improvements
##make it so you don't need to /suggest, the bot will automatically track it
##send a confirmation message when it does
##make it so whatever format it is in will still work

client = discord.Client()
TOKEN = open("TOKEN.txt").read()
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

spreadsheetID_Form = '1f2dYZzk6dLwbwJ4ycfGSqRS7GLEe2gg59JWaoeGtxeg'
range_Form = 'Sheet1!A1:H'

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


service = main()
sheet = service.spreadsheets()



def writeToOpen(toWrite,name):
    global sheet
    counter = 1
    for row in sheet.values().get(spreadsheetId=spreadsheetID_Form, range="Sheet1!A1:H").execute().get('values',[]):
        if row[0] == "":
            break
        counter += 1
    sheet.values().update(spreadsheetId=spreadsheetID_Form, range="A"+str(counter)+":I"+str(counter),valueInputOption='RAW',body={"range":"A"+str(counter)+":I"+str(counter),"majorDimension":'ROWS',"values":[getDataFromMessage(toWrite,name)]}).execute()


def getDataFromMessage(string,name):

    ## CARD FORMAT ##
    # Card Name
    # Rarity
    # Cat - Subcat
    # Energy/Power
    #
    # Ability Name
    # Ability
    data = []
    stringsplits = string.split("\n")
    data.append(stringsplits[0]) #name of card
    data.append(stringsplits[1]) #rarity
    data.append(stringsplits[2].split(" - ")[0]) #category
    data.append(stringsplits[2].split(" - ")[1]) #subcat
    data.append(stringsplits[3].split("/")[0]) #energy
    data.append(stringsplits[3].split("/")[1]) #power
    data.append(stringsplits[5]) #ability name
    data.append(stringsplits[6]) #ability text
    data.append(name)
    return data

@client.event
async def on_message(message):
    
    if message.content.count("\n")>4 and message.channel.id == '662645515665539134':
        if (message.content.split("\n")[4] == "" and " - " in message.content.split("\n")[2] and "/" in message.content.split("\n")[3]):
            writeToOpen(message.content,message.author.display_name)
            await message.channel.send("Added your card!")
        else:
            await message.channel.send("Suggestion is using the wrong format: check the pinned messages for the right one.")

@client.event
async def on_ready():
    print('ready')

client.run(TOKEN)
