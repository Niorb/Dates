# usr/bin/env python3

import bs4
from bs4 import BeautifulSoup
import requests
import random
from colorama import Fore, Style, init
import argparse
init()

parser = argparse.ArgumentParser()

parser.add_argument(
    "-b", "--blank", help="Doesn't save your results to a file and also asks for the dates you already know", action="store_true")
parser.add_argument(
    "-r", "--reset", help="Reset your known dates lists", action="store_true")
parser.add_argument(
    "-p", "--period", help="Only study dates out of one the specific periods or main chapters of time", action="store_true"
)
parser.add_argument(
    "-a", "--all", help="Study dates out of all the periods", action="store_true"
)

args = parser.parse_args()

page = requests.get(
    "http://keepschool.com/fiches-de-cours/college/histoire/grandes-dates-histoire.html#")
soup = BeautifulSoup(page.text, features="lxml")
rightList = []
secondRightList = []
blank = False
finalArray = []
counter = 0
secondCounter = 0
title = ""
element = soup.find("h4")
periods = []
events = []

# Setup events array and periods array
while True:
    if isinstance(element, bs4.element.Tag):
        if element.name == 'h4':
            title = element.text[:-1].strip()
            periods.append(title)
        elif element.name == 'ul':
            for event in element.find_all("li"):
                event = event.text
                columnIndex = event.find(":")
                el = {
                    "period": title,
                    "date": event[:columnIndex-1].strip(),
                    "event": event[columnIndex+2:].replace("\r", "").replace("\n", "").strip()
                }
                events.append(el)
    try:
        element = element.nextSibling
    except AttributeError:
        break

if args.reset:
    with open("./lists/rightList", 'w+') as file:
        file.write("")
    with open("./lists/secondRightList", 'w+') as file:
        file.write("")
if args.blank:
    blank = True
# Setup basicList,rightList,secondRightList
else:
    try:
        with open("./rightList", "r") as file:
            indexsToRemove = []
            for line in file.readlines():
                line = line.strip()
                for index, event in enumerate(events):
                    if line == event['event']:
                        indexsToRemove.append(index)
            indexsToRemove.sort(reverse=True)
            for index in indexsToRemove:
                rightList.append(events[index])
                events.pop(index)
    except FileNotFoundError:
        with open("./righlist", "w+") as file:
            file.write("")
        with open("./secondRightList", 'w+') as file:
            file.write("")

    with open("./secondRightList", "r+") as file:
        indexsToRemove = []
        for line in file.readlines():
            line = line.strip()
            for index, event in enumerate(events):
                if line == event['event']:
                    indexsToRemove.append(index)
        indexsToRemove.sort(reverse=True)
        for index in indexsToRemove:
            secondRightList.append(events[index])
            events.pop(index)


# Start asking questions
while True:
    print(str(len(rightList)+len(secondRightList))+"/204")
    if counter != 5:
        question = random.randint(0, len(events)-1)
        event = events[question]
        print("Thème: "+Fore.CYAN+event['period'], Style.RESET_ALL)
        print('Evènement: '+Fore.YELLOW+event['event'], Style.RESET_ALL)
        givenDate = input("Date: ")
        if givenDate == event['date']:
            counter += 1
            print(Fore.GREEN+"Correcte !")
            with open("./rightlist", 'a') as file:
                file.write(event['event']+"\n")
            rightList.append(event)
            events.pop(question)
        else:
            print(Fore.RED+'Incorrecte'+Style.RESET_ALL +
                  ', cela a eu lieu en', Fore.BLUE, event['date'])
        print(Style.RESET_ALL)
    elif counter == 5 and secondCounter != 4:
        counter = 0
        secondCounter += 1
        question = random.randint(0, len(rightList)-1)
        event = rightList[question]
        print("Thème: "+Fore.CYAN+event['period'], Style.RESET_ALL)
        print('Evènement: '+Fore.YELLOW+event['event'], Style.RESET_ALL)
        print(event['date'])
        givenDate = input("Date: ")
        if givenDate == event['date']:
            print(Fore.GREEN+"Correcte !")
            with open("./secondRightList", 'a') as file:
                file.write(event['event']+"\n")
            secondRightList.append(event)
            rightList.pop(question)
        else:
            print(Fore.RED+'Incorrecte'+Style.RESET_ALL +
                  ', cela a eu lieu en', Fore.BLUE, event['date'])
        print(Style.RESET_ALL)
    else:
        counter = 0
        secondCounter = 0
        question = random.randint(0, len(secondRightList)-1)
        event = secondRightList[question]
        print("Thème: "+Fore.CYAN+event['period'], Style.RESET_ALL)
        print('Evènement: '+Fore.YELLOW+event['event'], Style.RESET_ALL)
        print(event['date'])
        givenDate = input("Date: ")
        if givenDate == event['date']:
            print(Fore.GREEN+"Correcte !")
        else:
            print(Fore.RED+'Incorrecte'+Style.RESET_ALL +
                  ', cela a eu lieu en', Fore.BLUE, event['date'])
        print(Style.RESET_ALL)
