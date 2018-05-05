import requests
import json
from config import *

def lambda_handler(event, context):

	def getUpdateCommand():
		'''
		Function to fetch the details of the user. Specifically, we want the chat ID. chatID will be processed
		in the function getChatID()
		'''
		call = 'getUpdates'
		response = requests.get(URL+call)
		response_json = response.json()
		return response_json

	def getChatID(resp):
		'''
		Get the chatID from the getUpdates's response.
		'''
		ids=[]
		for id in resp['result']:
			if id['message']['chat']['id'] not in ids:
				ids.append(id['message']['chat']['id'])
		return ids

	def telegramMessage(chatID,quote,author):
		'''
		Send the random quote fetched in getRandomQuote function to telegram via POST
		'''
		call = 'sendMessage'
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
		for chatid in chat_ids:
			telegramMessage(chatid,quote,author)

# if __name__ == '__main__':
	main()