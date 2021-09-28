#! /usr/bin/env python3

import json
import random
import requests
import os
from pprint import pprint
from twilio.rest import Client
from termcolor import colored

# FILE_BASE = '/home/arun/amma-live-checker'
FILE_BASE = '.'
SENT_FILE = FILE_BASE + '/sent'
TWILIO = FILE_BASE + '/.twilio'

NUMBERS = [
    '+17343584745',
]

def giphy(search='sloth'):
    response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=TwtbpypGfzohlVWSNGg3m2xjpctAadad&limit=10')
    data = json.loads(response.text)
    num_choices = len(data['data'])

    for choice in range(num_choices):
        if not os.path.exists(SENT_FILE):
            ofile = open(SENT_FILE, 'w')
            ofile.close()

        sent = open(SENT_FILE, 'r').read().split(',')
        gif = data['data'][choice]
        if gif['id'] in sent:
            print(colored('Skipping {}'.format(gif['id']), 'red'))
            continue
        send_message(gif['images']['original']['url'])
        print(colored('Sent new GIF {}'.format(gif['id']), 'green'))
        sent.append(gif['id'])
        ofile = open(SENT_FILE, 'w')
        ofile.write(','.join(sent))
        ofile.close()
        break

def send_message (msg, numbers=NUMBERS):
    account_sid = 'AC1a7fd9b370e1c9a238288089f1da025e'
    auth_token = open(TWILIO, 'r').read()
    client = Client(account_sid, auth_token)

    for number in numbers:
        message = client.messages.create(
            body=msg,
            from_='+17344363993',
            to=number,
        )

giphy()
