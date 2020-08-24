from requests import get
from bs4 import BeautifulSoup
from time import sleep
import gmail_config
import smtplib

# sensitive info stored in config file
password = gmail_config.password
gmail = gmail_config.gmail

user_url = input('Paste your Amazon url and hit enter: ').strip() # strip to avoid any possible whitespace errors
head = gmail_config.header # find 'your user agent' on google and enter as a dict- e.g. head = {'User-Agent': 'your user agent here'}


def price_check():
    
    url = user_url
    req = get(url, headers = head)
    html = BeautifulSoup(req.text, 'html.parser')

    # Currently unused
    product = html.find(id = 'productTitle') # avoid errors from timing out
    if(product):
        product = product.text.strip()

    # Html is different when an Amazon item has no current sale
    # this avoids an error if there is no current sale and allows the program to continue running
    retail_price = html.find(class_ = 'priceBlockStrikePriceString a-text-strike')
    if(retail_price):
        retail_price = retail_price.text.strip() # strip to avoid errors from random whitespace
        retail_price = float(retail_price[1:])

    # Same error-avoidance as for retail_price
    curr_price  = html.find(id = 'priceblock_ourprice')
    if(curr_price):
        curr_price = curr_price.text.strip()
        curr_price = float(curr_price[1:])

    if(curr_price and retail_price and curr_price < retail_price):
        email()
    else:
        print('No current sale')


def email():

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail, password)

    subject = 'Amazon sale search response'
    body = f'View your item: {user_url}'
    msg = f'Subject: {subject}\n\n{body}' # 2 new lines for proper formatting

    # email yourself the url 
    server.sendmail(gmail, gmail, msg)

    print('Email was sent')


# Can check throughout the day by running once
while(True):
    price_check()
    sleep(86400) # Can set your check frequency - set to 24hrs by default
    