# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 22:33:25 2017

@author: LordKratos
"""

###############################################################################
#################################LIBRARIES USED################################
###############################################################################
from urllib.request import urlopen
from bs4 import BeautifulSoup
###############################################################################
################################CURRENCY CONVERTER#############################
###############################################################################
def currency_converter(currency_1,currency_2):
    url='http://www.xe.com/currencyconverter/convert/?Amount=1&From='+currency_1+'&To='+currency_2
    url=urlopen(url)
    bs=BeautifulSoup(url,'lxml')
    currency=bs.find('span',{'class':'uccResultAmount'}).string
    return currency
###############################################################################
############################CRYPTO CURRENCY PART###############################
###############################################################################
crypto = urlopen("https://coinmarketcap.com/")
soup=BeautifulSoup(crypto,"lxml")
positive="no-wrap percent-24h positive_change text-right"
negative="no-wrap percent-24h negative_change text-right"
i=1
mobile=0
crypto_list=soup.tbody.findAll("tr",{"class":""})
status=[]
for strings in crypto_list:
    name=strings.find("a",{"class":"currency-name-container"}).string
    price=strings.find("a",{"class":"price"}).string
    change=strings.find("td",{"class":positive})
    if(change==None):
        real_change=strings.find("td",{"class":negative})
        change=strings.find("td",{"class":negative}).string
    else:
        real_change=strings.find("td",{"class":positive})
        change=strings.find("td",{"class":positive}).string
    if(name=='Bitcoin' or name=='Ethereum' or name=='Ripple'):
        status.append([name,price,change])
        continue
    if(float(real_change.attrs["data-usd"])>=10.00):
        status.append([name,price,change])
    elif(float(real_change.attrs["data-usd"])<=-1.00):
        status.append([name,price,change])
    i=i+1
    if(len(status)==10):
        break

rupees=float(currency_converter('USD','INR'))

for i in range(len(status)):
    print('|',status[i][0],'| Price -> ',status[i][1],'  Rs.',float(status[i][1][1:])*rupees,'| Change -> ',status[i][2],'|')
    print("--------------------------------------------------------------------------------------")







