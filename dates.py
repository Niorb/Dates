# usr/bin/env python3

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

if args.reset:
    with open("./rightList", 'w+') as file:
        file.write("")
    with open("./secondRightList", 'w+') as file:
        file.write("")
if args.blank:
    blank = True
else:
    try:
        with open("./rightList", "r") as file:
            for line in file.readlines():
                line = line.strip()
                elementCount = 0
                finalElement = {}
                while line != "":
                    index = line.index("%")
                    if elementCount == 0:
                        finalElement["country"] = line[:index].strip()
                    elif elementCount == 1:
                        finalElement["capital"] = line[:index].strip()
                    elif elementCount == 2:
                        finalElement["memo"] = line[:index].strip()
                    else:
                        finalElement["continent"] = line[:index].strip()
                    index = index+1
                    elementCount = elementCount+1
                    line = line[index:]
                rightList.append(finalElement)
    except FileNotFoundError:
        with open("./righlist", "w+") as file:
            file.write("")
        with open("./secondRightList", 'w+') as file:
            file.write("")

    with open("./secondRightList", "r+") as file:
        for line in file.readlines():
            line = line.strip()
            elementCount = 0
            finalElement = {}
            while line != "":
                index = line.index("%")
                if elementCount == 0:
                    finalElement["country"] = line[:index].strip()
                elif elementCount == 1:
                    finalElement["capital"] = line[:index].strip()
                elif elementCount == 2:
                    finalElement["memo"] = line[:index].strip()
                else:
                    finalElement["continent"] = line[:index].strip()
                index = index+1
                elementCount = elementCount+1
                line = line[index:]
            secondRightList.append(finalElement)

finalArray = []
counter = 0
secondCounter = 0
elements = soup.find_all("h4")
periods = []
# Some useless information in that elements list (promotional titles, random information,...)
elements = elements[:-8]
for element in elements:
    ul = element.find_next("ul")
    dates = ul.find_all("li")
    periods.append(element.text[:-1].strip())
    for date in dates:
        date = date.text
        columnIndex = date.find(":")
        el = {
            'period': element.text[:-1].strip(),
            "date": date[:columnIndex-1].strip(),
            "event": date[columnIndex+2:].replace("\r", "").replace("\n", "").strip()
        }
        finalArray.append(el)
while True:
    if not blank:
        print(counter)
        print("Right: ", len(rightList), "Confirmed: ", len(secondRightList),
              "Total: ", len(rightList)+len(secondRightList), "/")
        if (secondCounter == 5 and counter == 3 and len(secondRightList) != 0):
            secondCounter = 0
            counter = 0
            question = random.randint(0, len(secondRightList)-1)
            el = secondRightList[question]
            print("Capitale de :", Fore.YELLOW +
                  el["country"]+Style.RESET_ALL)
            answer = input()
            if(answer == el["capital"].strip()):
                print("Right answer ! the continent is: " +
                      Fore.CYAN + el["continent"]+Style.RESET_ALL)
                print("Memo:" + Fore.RED +
                      el["memo"]+"\n"+Style.RESET_ALL)
                secondRightList.pop(question)
                continue
            else:
                print("\nFalse, the answer is: "+Fore.GREEN,
                      el["capital"], Style.RESET_ALL+"in: ", Fore.CYAN, el["continent"]+Style.RESET_ALL)
                string = str(el["country"]+"%"+el["capital"]+"%" +
                             el["memo"]+"%"+el["continent"]+"%\n")
                print("Memo: ", Fore.RED +
                      el["memo"], "\n", Style.RESET_ALL)
                with open("./secondRightList", 'r') as secondRightFile:
                    lines = secondRightFile.readlines()
                with open("./secondRightList", 'w') as secondRightFile:
                    for line in lines:
                        if line != string:
                            secondRightFile.write(line)
                with open("./rightList", 'a') as rightFile:
                    rightFile.write(string)
                secondRightList.pop(question)
                rightList.append(el)
                continue

        elif counter == 3 and len(rightList) != 0:
            counter = 0
            secondCounter = secondCounter+1
            question = random.randint(0, len(rightList)-1)
            el = rightList[question]
            print("Capitale de :", Fore.YELLOW +
                  el["country"]+Style.RESET_ALL)
            answer = input()
            if(answer == el["capital"].strip()):
                print("Right answer ! the continent is: " +
                      Fore.CYAN + el["continent"]+Style.RESET_ALL)
                print("Memo:" + Fore.RED +
                      el["memo"]+"\n"+Style.RESET_ALL)
                string = str(el["country"]+"%"+el["capital"]+"%" +
                             el["memo"]+"%"+el["continent"]+"%\n")
                with open("./secondRightList", 'a') as file:
                    secondRightList.append(el)
                    file.write(string)
                with open("./rightList", 'r') as rightfile:
                    lines = rightfile.readlines()
                with open("./rightList", 'w') as rightFile:
                    for line in lines:
                        if line != string:
                            rightFile.write(line)
                rightList.pop(question)
                continue
            else:
                print("\nFalse, the answer is: "+Fore.GREEN,
                      el["capital"], Style.RESET_ALL+"in: ", Fore.CYAN, el["continent"]+Style.RESET_ALL)
                print("Memo: ", Fore.RED +
                      el["memo"], "\n", Style.RESET_ALL)
                with open("./rightList", 'r') as rightfile:
                    lines = rightfile.readlines()
                with open("./rightList", 'w') as rightFile:
                    string = str(el["country"]+"%"+el["capital"]+"%" +
                                 el["memo"]+"%"+el["continent"]+"%\n")
                    for line in lines:
                        if line != string:
                            rightFile.write(line)
                rightList.pop(question)
                finalArray.append(el)
                continue
        else:
            question = random.randint(0, len(finalArray)-1)
            el = finalArray[question]
            print("Capitale de :", Fore.YELLOW +
                  el["country"]+Style.RESET_ALL)
            answer = input()
            if(answer == el["capital"].strip()):
                counter = counter+1
                print("Right answer ! the continent is: " +
                      Fore.CYAN + el["continent"]+Style.RESET_ALL)
                print("Memo:" + Fore.RED +
                      el["memo"]+"\n"+Style.RESET_ALL)
                with open("./rightList", "a") as file:
                    string = str(el["country"]+"%"+el["capital"]+"%" +
                                 el["memo"]+"%"+el["continent"]+"%\n")
                    rightList.append(el)
                    file.write(string)
                finalArray.pop(question)
                continue
            else:
                print("\nFalse, the answer is: "+Fore.GREEN,
                      el["capital"], Style.RESET_ALL+"in: ", Fore.CYAN, el["continent"]+Style.RESET_ALL)
                print("Memo: ", Fore.RED +
                      el["memo"], "\n", Style.RESET_ALL)
                continue
    else:
        question = random.randint(0, len(finalArray)-1)
        el = finalArray[question]
        print("Capitale de :", Fore.YELLOW +
              el["country"]+Style.RESET_ALL)
        answer = input()
        if(answer == el["capital"].strip()):
            print(len(finalArray)+"/199")
            counter = counter+1
            print("Right answer ! the continent is: " +
                  Fore.CYAN + el["continent"]+Style.RESET_ALL)
            print("Memo:" + Fore.RED+el["memo"]+"\n"+Style.RESET_ALL)
            finalArray.pop(question)
            continue
        else:
            print("\nFalse, the answer is: "+Fore.GREEN,
                  el["capital"], Style.RESET_ALL+"in: ", Fore.CYAN, el["continent"]+Style.RESET_ALL)
            print("Memo: ", Fore.RED+el["memo"], "\n", Style.RESET_ALL)
            continue
