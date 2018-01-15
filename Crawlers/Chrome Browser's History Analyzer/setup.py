# -*- coding: utf-8 -*-
"""
@author: LordKratos
"""

###############################################################################
#################################LIBRARIES USED################################
###############################################################################
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import sqlite3
import os
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt
###############################################################################
################################FUNCTIONS######################################
###############################################################################

def analyze(results): 
	prompt = input("Type <c> to print or <p> to plot\n")
	if prompt == "c":
		for site, count in sites_count_sorted.items():
			print(site, count)
	elif prompt == "p":
		plt.bar(range(len(results)), results.values(), align='edge')
		plt.xticks(rotation=45)
		plt.xticks(range(len(results)), results.keys())
		plt.show()
	else:
		print("Choose the correct one!")
		quit()

def parse(url):
 	try:
 		parsed_url_components = url.split('//')
 		sublevel_split = parsed_url_components[1].split('/', 1)
 		domain = sublevel_split[0].replace("www.", "")
 		return domain
 	except IndexError:
 		print("URL format error!")
###############################################################################
####################PATH TO USER'S HISTORY DATABASE############################
###############################################################################
if 'Linux' in os.uname():
#	'Linux Distro!!'
	try:
		history_db = os.path.expanduser('~')+'/.config/google-chrome/Default/history'
		files = os.listdir(history_db)
	except FileNotFoundError:
		try:
			history_db = os.path.expanduser('~')+'/.config/chromium/Default/history'
		except FileNotFoundError:
			print("No such path! Give the right path.")
			history_db = input()
			pass
else:
#	'Windows!!'
	try:
		history_db = os.path.expanduser('~')+r"\AppData\\Local\Google\Chrome\User Data\Default\history"
		files = os.listdir(history_db)
	except FileNotFoundError:
		print("No such path! Give the right path.")
		history_db = input()
		pass

###############################################################################
#######################QUERYING THE DATABASE###################################
###############################################################################
c = sqlite3.connect(history_db)
cursor = c.cursor()
select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
cursor.execute(select_statement)

results = cursor.fetchall()

sites_count = {}
###############################################################################
###################################LASTLY######################################
###############################################################################
for url, count in results:
	url = parse(url)
	if url in sites_count:
		sites_count[url] += 1
	else:
		sites_count[url] = 1
 
sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
 
analyze (sites_count_sorted)

