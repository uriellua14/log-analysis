from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import os
import tarfile
from art import *
from colorama import Fore, Back, Style
from colorama import init
import re
import pandas as pd
import openpyxl
from itertools import groupby 
import matplotlib.pyplot as plt
from pathlib import Path
import shutil
#################################################################
init(convert=True)
#pint program name
tprint('<<<Tar Analysis 2.0>>>')
#ask for folder name
print(Fore.CYAN) 
name = input("Please enter the Tar folder name:")
print(Style.RESET_ALL)
##thammarak get home directory
home = str(Path.home())
download_path = os.path.join(home, "Downloads\\")
#so we dont have to tipe .tar.gz
namet = name + ".tar.gz"
path = os.path.join(download_path, namet)
nameU = name+'unzip'
#open and unzip tar folder
tar = tarfile.open(path,"r:gz")
tar.extractall()
tar.close()
os.mkdir(nameU)
#### to unzip files inside zip folder:)
for i in os.listdir(name):
    foldername = os.path.join(name, i)
    os.makedirs(i)
    y = tarfile.open(foldername,"r:gz")
    y.extractall(i)
    y.close()
    shutil.move(i,nameU)
     
################################################################
#CLI to ask what errors to look for 
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336',
    Token.Question: '',
})
questions = [
    {
        'type': 'checkbox',
        'message': 'Please select errors to look for',
        'name' : 'variables',
        'choices': [
            Separator('= Errors to look for ='),
            {
                'name': 'FAILED VALIDATION!!',
                'checked': True
            },
            {
                'name': 'FAILED VALIDATION while executing command',
            },
            {
                'name': 'FAILED VALIDATION - Reported',
            },
            {
                'name': 'FAILED - COMMAND TIMED OUT',
            },
            {
                'name': 'Test(s) failed:',
            },
            {
                'name': '***err',
            },
            {
                'name': 'FAIL**',
            },
            {
                'name': 'err-disable',
            },
            {
                'name': 'Write your own',
            },
            {
                'name': 'RegEx query',
            },
             {
                'name': '->Make Excel report',
            },
            Separator('= Enter a Command and print switch log for it ='),
            {
                'name': 'Enter Command :',
            },
        ],
        'validate': lambda answer: 'You must choose at least one error to look for.' \
            if len(answer) == 0 else True
    }
]

answers = prompt(questions, style=style)
###################################################################
#reads for new entry "write yout own"
if 'Write your own' in answers["variables"]:
    own = input("Please enter the error you are looking for: ")
    answers["variables"] = [own if i=='Write your own' else i for i in answers["variables"]]
###################################################################
#reads for new entry "write yout own"
if 'RegEx query' in answers["variables"]:
    regex = input("Please enter the regex pattern to search for: ")
    regex = r"{}".format(regex)
    answers["variables"] = [regex if i=='RegEx query' else i for i in answers["variables"]]
    regex_flag = True
else: regex_flag = False

###################################################################
#opens all the files and writes line by line in log.txt document
logs = open('logs.txt',"w+")
for path,subdirs,files in os.walk(nameU):
        for i in files:
            filename = os.path.join(path, i)
            ### writing to text file
            with open(filename) as infile:
                for line in infile:
                    logs.write(line)
####################################################################
#reads text file to find corners  
cornerCount1 = 0
corner1=[]
with open("logs.txt") as L:
    for line in L:
        if 'Corner Name :' in line and 'PST' not in line and 'PDT' not in line:
            cornerCount1 +=1
###################################################################
#reads for new entry "Enter Command"
cmdDo = 0
if 'Enter Command :' in answers["variables"]:
    cmd = input("please enter Command to output log:")
    print ('There are ' ,cornerCount1,'corners,  Example for entry : 1 2 3 ')
    cornerPrint1 = input("Write the number of corner separated by a space(type 0 for all):")
    cornerPrint = cornerPrint1.split()
    #makes list int
    for i in range(0, len(cornerPrint)): 
        cornerPrint[i] = int(cornerPrint[i]) 
    ##looks for next comand to know where to stop
    
    with open("logs.txt") as C: 
        for line in C:
            line = line.split(",",1)
            if cmdDo == 1: 
                cmdEnd = line[0]
                cmdDo = 0
            if cmd in line:
                cmdDo = 1
###################################################################
#look up for errors line by line 
#varibles
count = 0
corner = ''
fails = []
switch = []
switchNumber = 'first777#$'
#opens text file to read
with open("logs.txt") as L:
    for line in L:
    # look for corner
        if 'Corner Name :' in line and 'PST' not in line and 'PDT' not in line and line not in corner:
            corner = line
            count = 0
            print(Fore.BLACK)
            print (Back.WHITE+'                     >  '+corner)
            print(Style.RESET_ALL)
    #Looks for Testcase number
        if 'TESTCASE START -' in line :
            testn = line
    # using re.py to search for switch number
        if 'TESTCASE START -' in line and switchNumber not in line:
            count = 0 
            switchNumber = re.search(r'\w\w\w\w\w\w\d(\d)?', line).group(0)
            print (Fore.GREEN+(switchNumber))
            print(Style.RESET_ALL)
    #adding to list with errors
        for i in answers["variables"]:
            if i in line and i not in fails:
                fails.append(line)
            elif regex_flag and re.search(i, line):
                fails.append(line)
        if len(fails) > 0 and 'TESTCASE END -' in line:
            count += 1
            print(Fore.YELLOW +str(count)+"--"+(testn))
            print(Style.RESET_ALL)
            print (*fails, sep = "\n")
    #clearing error list
        if 'TESTCASE END -' in line:
            fails.clear()
#################################################################
#looking for command output log
cmdLog = []
cmdStart = 10000000
ii = 0
full = 0
cornerCount = 0
switchNumber1 = 'first777#$'
if 'Enter Command :' in answers["variables"]:
    cmd = cmd + ' '
    print(Fore.BLACK)
    print (Back.RED+'Command Log Output')
    print(Style.RESET_ALL)
    with open("logs.txt") as B:
        for line in B:
            ii += 1
    # look for corner
            if 'Corner Name :' in line and 'PST' not in line and 'PDT' not in line and line not in corner:
                corner = line
                count = 0
                cornerCount += 1 
                print(Fore.BLACK)
                print (Back.WHITE+'                     >  '+corner)
                print(Style.RESET_ALL)
    #Looks for Testcase number
            if 'TESTCASE START -' in line :
                testn = line
    # using re.py to search for switch number
            if 'TESTCASE START -' in line and switchNumber1 not in line:
                count = 0
                switchNumber1 = re.search(r'\w\w\w\w\w\w\d(\d)?', line).group(0)
                print (Fore.GREEN+(switchNumber1))
                print(Style.RESET_ALL)
    # looking for comand output
            if cmd in line and line not in cmdLog:
                cmdLog.append(line)
                cmdStart = ii
                cmdStop = 10000000
                full = 1
            if ii >= cmdStart and ii < cmdStop and line not in cmdLog:
                cmdLog.append(line)
            if cmdEnd in line or 'Done executing all the given commands' or 'Finished executing command:' in line:
                cmdStop = ii
            #print command output
            if 'TESTCASE END' and full == 1:
                for i in cornerPrint:
                    if i == cornerCount or i == 0:
                        cmdLog = list(filter(None, cmdLog))
                        print(*cmdLog, sep = "\n")
                        cmdLog.clear()
                        full = 0
#################################################################
#this part is to make an excel report on test
##variables
testName = []
jobID = []
nameEx = name + ".xlsx"
one = []
two = []
three = []
testExcel = []
switchExcel = 'first777#$'
failsE = []
cornerE = ''
####
four = []
fourCorner = ''
fourSwitch = 'first777#$'
fourFails = 0
do = 0
sfp = []
sfpee = str("sfpee  ")
sfpSwitch = 'first777#$'
sfpCorner = 0
sfpCount2 = 0
switch_count = []
countE=0
#makes first sheet in excel - Test info
if '->Make Excel report' in answers["variables"]:
    with open("logs.txt") as E:
        for line in E:
            if "Starting Job Id " in line and len(one)<1:
                one.append(line)
            if "job_name" in line and  len(one)<2:
                one.append(line)
            if "MODEL_NUM" in line and line not in one:
                one.append(line)
            if "MOTHERBOARD_SERIAL_NUM" in line and line not in one:
                one.append(line)
            if "SYSTEM_SERIAL_NUM" in line and line not in one:
                one.append(line)
            # look for corner
############ add sfp info to SFP sheet in excel 
            if 'TESTCASE START -' in line and sfpSwitch not in line:
                sfpSwitch = re.search(r'\w\w\w\w\w\w\d(\d)?', line).group(0)
                if sfpSwitch not in switch_count:
                    switch_count.append(sfpSwitch)
            if '{sfpee}' in line:
                sfpCount2 += 1
                if sfpCount2 <= len(switch_count):
                    sfp.append('*************************************************')
                    sfp.append(sfpSwitch)
                    sfp.append('*************************************************')
            if "EEPROM in port" in line and sfpCount2 <= len(switch_count):
                sfp.append(line)
            if " Transceiver" in line and sfpCount2 <=  len(switch_count):
                sfp.append(line)
            if " Vendor PN" in line and sfpCount2 <= len(switch_count):
                sfp.append(line)
            if " Vendor SN" in line and sfpCount2 <=  len(switch_count):
                sfp.append(line)
            if " Extended ID" in line and sfpCount2 <=  len(switch_count):
                sfp.append(line)
############ add errors to second sheet in excel 
            if 'Corner Name :' in line and 'PST' not in line and 'PDT' not in line and line not in corner:
                cornerE = line
                countE = 0
                two.append(cornerE)
                fourCorner = re.search(r"\{.*?}", line).group(0)
            #Looks for Testcase number
            if 'TESTCASE START -' in line :
                testExcel = line
            # using re.py to search for switch number
            if 'TESTCASE START -' in line and switchExcel not in line:
                switchExcel = re.search(r'\w\w\w\w\w\w\d(\d)?', line).group(0)
                fourSwitch = switchExcel
                two.append(switchExcel)
            #adding to list with errors
            for i in answers["variables"]:
                if i in line and i not in failsE:
                    failsE.append(line)
                    fourFails += 1
                elif regex_flag and re.search(i, line):
                    failsE.append(line)
                    fourFails += 1
            if len(failsE) > 0 and 'TESTCASE END -' in line:
                countE += 1
                testExcel = str(countE) + "--" + testExcel
                two.append(testExcel)
                two.extend(failsE)
                ### to make a graph
                four.append(fourCorner)
                four.append(fourSwitch)
                four.append(countE)
                four.append(fourFails)
            #clearing error list
            if 'TESTCASE END -' in line:
                failsE.clear()
###########################################################
#### graph to excel
#varibles
count_graph = 0
corner = ''
fails = []
switch = []
testcase_graph = 'first777#$'
switchNumber_graph = 'first777#$'
switch_graph1 = []
group_graph = []
#opens text file to read
with open("logs.txt") as L:
    for line in L:
    # look for corner
        if 'TESTCASE START ' in line and 'Testcase' in line and 'PDT' in line or 'PST' in line:
            if count_graph >= 1:
                switch_graph1 = [switchNumber_graph +" - "+ testcase_graph,'YES']
            else:
                switch_graph1 = [switchNumber_graph +" - "+ testcase_graph,'no']
            switchNumber_graph = re.search(r'\w\w\w\w\w\w\d(\d)?', line).group(0)
            testcase_graph = line[line.index('{') + len('{'):]
            testcase_graph = testcase_graph.replace('}\n',"")
            switchNumber_graph = re.sub("[^0123456789\.]","",switchNumber_graph)
            count_graph = 0
            group_graph.append(switch_graph1)
        for i in answers["variables"]:
            if i in line:
                count_graph += 1
#################################################################
## makes the data for the graph nicer 
## makes the data for the graph nicer 
group_graph.pop(0)
group_graphD = pd.DataFrame(group_graph, columns = ['switch - Testcase','error'])
group_graph_count = group_graphD.pivot_table(index=['switch - Testcase','error'], aggfunc='size')
###########################################################
############add commannd log if any to third sheet in excel 
#variables
cmdLogE = []
cmdStartE = 10000000
iE = 0
fullE = 0
cornerLE = ''
switchNumber1E = 'first777#$'
three = []
cornerCountE = 0
if 'Enter Command :' in answers["variables"]:
    with open("logs.txt") as B:
        for line in B:
            iE += 1
            # look for corner
            if 'Corner Name :' in line and 'PST' not in line and 'PDT' not in line and line not in cornerLE:
                cornerLE = line
                cornerLE = '---------------'+ cornerLE
                countLogE = 0
                cornerCountE += 1
                three.append(cornerLE)
            #Looks for Testcase number
            if 'TESTCASE START -' in line :
                testLog = line
            # using re.py to search for switch number
            if 'TESTCASE START -' in line and switchNumber1E not in line:
                countLogE = 0 
                switchNumber1E = re.search(r'\w\w\w\w\w\w\d(\d)?', line).group(0) 
                three.append(switchNumber1E)
            # looking for comand output
            if line.startswith(cmd) and line not in cmdLogE:
                cmdLogE.append(line)
                cmdStartE = iE
                cmdStopE = 10000000
                fullE = 1
            if iE >= cmdStartE and iE < cmdStopE and line not in cmdLogE:
                cmdLogE.append(line)
            if cmdEnd in line or 'Done executing all the given commands' in line:
                cmdStopE = iE
            #print command output
            if 'TESTCASE END' and fullE == 1:
                for i in cornerPrint:
                    if i == cornerCountE or i == 0:
                        cmdLogE = list(filter(None, cmdLogE))
                        three.extend(cmdLogE)
                        cmdLogE.clear()
                        fullE = 0
################################################################
#print to excel
if len(one)>0:
    one = pd.Series(one)
if len(two)>0:
    two = pd.Series(two)
if 'Enter Command :' in answers["variables"]:
    three = pd.Series(three)
if len(four)>0:
    four = pd.Series(four)
if len(sfp)>0:
    sfp = pd.Series(sfp)
w = pd.ExcelWriter(nameEx)
if '->Make Excel report' in answers["variables"]:
    one.to_excel(w,'Test Info')
    two.to_excel(w,'Test Errors')
    if 'Enter Command :' in answers["variables"]:
        three.to_excel(w,'Command Log')
    if len(group_graphD)>0:
        group_graph_count.to_excel(w,'Testcase Error')
    if len(sfp)>0:
        sfp.to_excel(w,'SFP')
    w.save()


