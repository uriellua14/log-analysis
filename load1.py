import tarfile
import os 
# open file
file = tarfile.open('25223.tar.gz')
  
# extracting file
file.extractall()
file.close 

for subdirs in ("25223"):
    for i in subdirs:
        i = tarfile.open(i,"r:gz")
        i.extractall()
        i.close()    


name = input("Please enter the Tar folder name:")
print(Style.RESET_ALL)
##thammarak get home directory
home = str(Path.home())
download_path = os.path.join(home, "Downloads\\")
#so we dont have to tipe .tar.gz
namet = name + ".tar.gz"
path = os.path.join(download_path, namet)
#open and unzip tar folder
tar = tarfile.open(path,"r:gz")
tar.extractall()
tar.close()
path1 = os.path.join(download_path, name)
for i in path1:
    foldername = os.path.join(path1, i)
    y = tarfile.open(foldername,"r:gz")
    y.extractall()
    y.close()    
