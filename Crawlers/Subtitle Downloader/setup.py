# -*- coding: utf-8 -*-
"""
@author: LordKratos
"""

###############################################################################
#################################LIBRARIES USED################################
###############################################################################
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import requests
from pyunpack import Archive
import os
import sys
###############################################################################
###########################MOVIE SELECTION#####################################
###############################################################################
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
print("Name the movie!!")
print('---------------------------------------------------------------------')
name=input().split()
c=1
movie_list=[]
try:
    search="https://subscene.com/subtitles/title?q="
    for i in range(1,len(name)):
        name[0]=name[0]+"+"+name[i]
    name=str(name[0])
    search=search+name+"&l="
    req0 = urllib.request.Request(search, headers = headers)
    page=urllib.request.urlopen(req0)
except HTTPError as e:
    print(e)
    sys.exit()
except URLError as e:
    print(e)
    sys.exit()

try:
    search_page=BeautifulSoup(page,"lxml")
    different_movies=search_page.body.findAll("li")
    print("Which one you wanna select?")
    print("")
    for movie in different_movies:
        if(movie.find("div",{"class":"title"})!=None):
            if(movie.find("div",{"class":"title"}).a!=None):
                print(c,"->",movie.find("div",{"class":"title"}).a.string)
                print('---------------------------------------------------------------------')
                movie_list.append(movie.find("div",{"class":"title"}).a.attrs["href"])
                c=c+1
except AttributeError as e:
    print(e)
    sys.exit()
try:
    movie_option=int(input())
except ValueError:
    print("Select the right option.")
###############################################################################
######################SPECIFIC SELECTION#######################################
###############################################################################
mod_url=0
url='https://subscene.com'+movie_list[movie_option-1]
print('Choose your movie quality!\n1)1080p\n2)720p\n3)480p')
choise=input()
if choise == '1':
    movie_quality='1080p'
elif choise == '2':
    movie_quality='720p'
elif choise == '3':
    movie_quality='480p'
else:
    sys.exit("Enter the correct option.")
print('Give more details!\nPress "Enter" if you don\'t know the details...')
details=input()
print('Encodings?')
encoding=input()
req = urllib.request.Request(url, headers = headers)
subs=urllib.request.urlopen(req)
subtitles=BeautifulSoup(subs,"lxml")
#print(subtitles)
language_subs=subtitles.tbody.findAll("a")
for language in language_subs:
    if(language.span!=None):
#        print(language.span.string.strip())
        if(language.span.string.strip()=='English'):
#            print(language.findAll("span")[1].string.strip().split(' '))
            english = language.findAll("span")[1].string.strip()
            split=english.split('.')
            if(len(split)<4):
                split=english.split(' ')
            if(movie_quality in split):
                if(details!=None and details in str(split).lower()):
                    if(encoding!=None and encoding in str(split).lower()):
#                        print(language.findAll("span")[1].string.strip())
                        mod_url=("https://subscene.com"+language.attrs["href"])
                        break
                    else:
#                        print(language.findAll("span")[1].string.strip())
                        mod_url=("https://subscene.com"+language.attrs["href"])
                        break
                else:
#                    print(language.findAll("span")[1].string.strip())
                    mod_url=("https://subscene.com"+language.attrs["href"])
                    break
if(mod_url==0):
    for language in language_subs:
        if(language.span!=None):
            if(language.span.string.strip()=='English'):
                mod_url=("https://subscene.com"+language.attrs["href"])
                break
#print(mod_url)
###############################################################################
#########################DOWNLOADING AND SAVING################################
###############################################################################
if mod_url == 0:
    #print("Oops!!No Subtitles Found!")
    sys.exit("Oops!!No Subtitles Found!")
print("Downloading...")
req1 = urllib.request.Request(mod_url, headers = headers)
sub_down=BeautifulSoup(urllib.request.urlopen(req1),"lxml")
#print(sub_down.find("div",{"class":"download"}).a.attrs["href"])
download="https://subscene.com"+sub_down.find("div",{"class":"download"}).a.attrs["href"]
downdown=requests.get(download)
try:
    downdown.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
    sys.exit()
#print(len(downdown.text))
#print(downdown.text)


try:
    savefile=open(r'/media/tony/LordKratos/GitHub Pojects/Crawlers/Subtitle Downloader/subs.rar','wb')
    for chunk in downdown.iter_content(100000):
        savefile.write(chunk)
    savefile.close()
    Archive(r'/media/tony/LordKratos/GitHub Pojects/Crawlers/Subtitle Downloader/subs.rar').extractall(r'/media/tony/LordKratos/GitHub Pojects/Crawlers/Subtitle Downloader')
    os.remove(r'/media/tony/LordKratos/GitHub Pojects/Crawlers/Subtitle Downloader/subs.rar')
    print("Download Complete!")
except ValueError:
    print("Path not found!")

