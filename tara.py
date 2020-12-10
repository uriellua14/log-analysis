
import os 
import tarfile
from colorama import Fore, Back, Style 
from colorama import init
init(convert=True)
#ask for folder name 
name = input("please enter the Tar folder name: ")
#so we dont have to tipe .tar.gz and we can open the folder when extracted
namet = name + ".tar.gz"
#open and unzip tar folder 
tar = tarfile.open(namet,"r:gz")
tar.extractall()
tar.close()


#opens all the files and writes line by line in log.txt document  
logs = open('logs.txt',"w+") 
for path, subdirs, files in os.walk(name):
        for i in files:
            filename = os.path.join(path, i)
            ### writing to text file 
            with open(filename) as infile:
                for line in infile:
                    logs.write(line)
            
#### analizing logs file 
failure = []
count = 0
corner = ''
fails = []
switch = []
switchNumber = 'first'
k= "switch"
with open("logs.txt") as L:
    for line in L:
        if 'Corner Name :' in line and 'PST' not in line and line not in corner:
            corner = line
            print (Back.CYAN+'  >  '+corner)
            print(Style.RESET_ALL)
        if 'TESTCASE START -' in line :
            testn = line
        if 'TESTCASE START -' in line and switchNumber not in line:
            switchNumber = testn.split(" ")[8]
            print (Back.WHITE+Fore.BLACK+(switchNumber))
            print(Style.RESET_ALL)
        if 'FAIL**' in line:
            failure.append(line)
        if 'FAILED VALIDATION' in line or 'FAILED w' in line:
            fails.append(line)
        if len(fails) > 0 and 'TESTCASE END -' in line: 
            count += 1
            print(Fore.YELLOW +str(count)+":"+(testn))
            print(Style.RESET_ALL)
            print (*fails, sep = "\n")
            print (*failure, sep = "\n")
    
        if 'TESTCASE END -' in line:
            #clearing error list
            fails.clear()
            failure.clear()

'''    
        '''