#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

"""
    @Author     : Harter·Liang
    @Time       : 2021/04/25
    @Description: A little calendar for display the "History in toady" events of the music
"""

import requests
from time import *
from bs4 import BeautifulSoup
import random
from datetime import datetime
from tkinter import *

req = requests.session()

url = 'https://www.thisdayinmusic.com/search/?keyword=&'

headers = {
    'Host': 'www.thisdayinmusic.com',
    'User-Agent': 'Mozilla/5.0 (Android 9.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Referer': 'https://www.thisdayinmusic.com/search/',
    'Cookie': '_ga=GA1.2.150240726.1608269437; _gid=GA1.2.213997004.1608269437; _gat_gtag_UA_13057011_1=1',
    'Upgrade-Insecure-Requests': '1'
}

'''
    For getting the raw information from the internet according to the link provided
    :param month: To specify the month we need
    :param day: To specify the day we need
    :return The raw information from the specific page decided by the link
'''


def getRawMes(month, day):
    count = 0
    # Concatenate the parameters to form the valid url
    payload = url + 'date=' + str(day) + '&month=' + str(month)

    res = req.get(url=payload, headers=headers)

    while res.status_code != 200 and count < 5:
        # For some unexpected situations
        print('OOPS,ready for retrying...')
        # Sleep for the further retry
        sleep(2)
        res = req.get(url=payload, headers=headers)
        count += 1

    if count >= 5:
        print('Network Error!')
        exit(0)

    return res.text


'''
    Pick the useful information from the raw information fetched from the website
    :param rawContent: The raw content from the internet by using the requests
    :return The collection list of the dictionary contains the date and the description of the event
'''


def pickMes(rawContent):
    soup = BeautifulSoup(rawContent, features="lxml")

    # The date of the event
    name = soup.find_all(class_='search-results-date')
    # The collection of the date
    names = []
    # The description of the event
    des = soup.find_all(class_='search-results-description')
    # The collection of the description
    desCollection = []
    final = []

    for i in name:
        names.append(i.text)
    for j in des:
        desCollection.append(j.text)

    length = len(names)

    for k in range(0, length - 1):
        result = {'Date': names[k], 'Describe': desCollection[k]}
        final.append(result)

    return final


'''
    For choose the dictionary contains the date and the description of the event randomly
    :param dicLists: The collection of the dictionary
    :return The random index for the list of the dictionary
'''


def makeDirect(dicLists):
    number = random.randint(0, len(dicLists))
    return dicLists[number]


'''
    The construction of the GUI is listed in this function, sadly, the whole process is learned from the internet
'''


def main():
    nowTime = datetime.now()
    day = nowTime.day
    month = nowTime.month
    contents = getRawMes(month, day)
    collection = pickMes(contents)
    result = makeDirect(collection)
    Dates = result['Date']
    Describe = result['Describe']

    root = Tk()
    root.title('Music Calendar')
    root.geometry('800x500')

    texts = 'Today is ' + str(nowTime.year) + '-' + str(month) + '-' + str(day)
    Label(root, text=texts.encode('utf8'), font=('Arial', 20)).pack()
    texts1 = 'What happened in the history of Music:'
    Label(root, text=texts1.encode('utf8'), font=('Arial', 15)).pack(side=TOP)

    frm = Frame(root)
    frm_L = Frame(frm)
    Label(frm_L, text='The Date is:'.encode('utf8'), font=('Arial', 15)).pack(side=TOP)
    frm_L.pack(side=LEFT)
    frm_R = Frame(frm)
    Label(frm_R, text=Dates.encode('utf8'), font=('Arial', 15)).pack(side=TOP)
    frm_R.pack(side=RIGHT)
    frm.pack()

    Sentences = str(Describe).split('. ')

    t = Text(root)
    count = 0
    for sen in Sentences:
        if count == len(Sentences) - 1:
            t.insert(END, sen + '\n')
        else:
            t.insert(END, sen + '.\n')
        count += 1
    t.pack()
    root.mainloop()


'''
    Original part of the main function, which is aimed at the implementation of the commandline mode...
def main():
    nowTime = datetime.now()
    day = nowTime.day
    month = nowTime.month
    contents = getRawMes(month,day)
    collection = pickMes(contents)
    print('[+] Today is '+str(nows.year)+'-'+str(month)+'-'+str(day))
    print('[+] What happened in the history of Music:')
    print()
    makeDirect(collection)
'''
if __name__ == "__main__":
    main()
