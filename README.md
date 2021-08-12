# log-analysis
I created this software so it would be easier for EDVT engineers to find patterns when looking for errors during testing using the log files from the test.
# This is how the program CLI looks after running
![image](https://user-images.githubusercontent.com/52641414/128780913-612bc9fe-7ed6-4161-860f-d4e9b71af2ea.png)

# This a example of how the errors are printed
In this Test only switch4 had problems 
 ![image](https://user-images.githubusercontent.com/52641414/128780974-14bcdbce-61f2-4df5-a2e3-348b19c1d104.png)


This program takes all the log files from the automated testing program we use in Cisco and merges them together in a text file that can be well over one million lines. I decided to merge all the files to have one single text document that contains all the information available from the test. This file includes the logs from all the equipment used in the test and the CSV files that automate the testing.

Then from there the CLI gives you options on what errors to look for and then prints out the found error and the exact location on the test where they where found, separating the errors printed by system number and test temperature. Some other abilities from the CLI program are:

Create an Excel report that includes the serial number of all the equipment being tested. Include all the errors found and the serial number and type and serial number of the parts of every switch. It uses a separated sheet inside the same Excel program for each type of search.
Use regex to look for specific results.
Write any text to Mach and give location.
Get the full log of any command used in the test.

## How to install
  1. Clone this repository - "git clone https://github.com/uriellua14/log-analysis.git" 

2. Download the log file to analyze

3. Install python, necesary libraries (requirements.txt), and run tara.py


## Enter on Windows Terminal to install necessary libraries and python

install python - "python"

download pip - "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"

install pip - "python get-pip.py"

install requirements - "pip install -r requirements.txt"



## Enter on Mac Terminal

install Xcode - "xcode-select --install"

download homebrew - "/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" "

install python - "brew install python3"

download pip - "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"

install pip = "python3 get-pip.py"

install requirements - "pip install -r requirements.txt"







