##################################################################
### 		      ***** Quotes Telegram *****    	       ###
##################################################################
### Author 	: Madhava Kulkarni			       ###
### E-mail 	: madhav.kulkarni1986@gmail.com                ###
### License : Free to use, modify and distribute	       ###
### For all the details and setup instructions, view README.md ###
##################################################################
import requests
import json
from config import *

''' 
from config import * -> is for importing or sourcing or including the variables that are required 
but should not be exposed(pun intended!) in the script.
TELEGRAMURL		-> Telegram API url
TELEGRAMTOKEN	-> Telegram API token
TALAIKIS 		-> Talaikis API to get random quotes
URL 			-> Combination of TELEGRAMURL and TELEGRAMTOKEN

PS: I could have defined some variables in this script, but defining in config looks clean ;-)
You have to include the config.py file for your script with the above described variables

'''

def lambda_handler(event, context):
	'''
		AWS Lambda's lambda_handler method which is called by the scheduler - cloudWatch
	'''
	def getUpdateCommand():
		'''
		Function to fetch the details of the user. Specifically, we want the chat ID
		chatID will be processed in the function getChatID()
		'''
		call = 'getUpdates' # Method or function to get the chat IDs and other details 
		response = requests.get(URL+call)
		response_json = response.json()
		return response_json

	def getChatID(resp):
		'''
		Get the chatID from the getUpdates's response.
		'''
		# Let's get all the IDs present in the bot
		ids=[]
		for id in resp['result']:
			if id['message']['chat']['id'] not in ids:
				ids.append(id['message']['chat']['id'])
		return ids

	def telegramMessage(chatID,quote,author):
		'''
		Telegram the random quote fetched in getRandomQuote method (POST method)
		'''
		call = 'sendMessage' # --> Method or function to telegram the quote to the users
		message = quote + "\nBy: " + author
		params = {'chat_id':chatID,'text': message}
		response = requests.post(URL+call,params)

	def getRandomQuote():
		'''
		Get a random quote from talaikis api
		'''
		quote_resp = requests.get(TALAIKIS)
		quote = quote_resp.json()['quote']
		author = quote_resp.json()['author']
		return quote,author

	def main():
		'''
		main function that does all the wheeling
		'''
		quote,author = getRandomQuote()
		getResp = getUpdateCommand()
		chat_ids = getChatID(getResp)
		
		# Iterate through all the IDs present in the bot and send them the quote
		for chatid in chat_ids:
			telegramMessage(chatid,quote,author)

	# Let's begin here
	main()
