import sys
import glob
import hashlib
import os
import csv

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
filenames = glob.glob(r'C:/Users/jkang/Documents/mentorshipWork/Geojsons/*.geojson')

data = []
empty = []
details = ["File Name", "Hash"]

for filename in filenames:
    name_hash = []
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        
        name_hash.append(filename)
        name_hash.append(sha256_hash.hexdigest())
        data.append(name_hash)

#print(data)
#print("\n")

with open('hashlist.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerow(details) 
    write.writerows(data) 

inputdata = []
with open('hashlist.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        inputdata_1 = []
        inputdata_1.append(row['File Name'])
        inputdata_1.append(row['Hash'])
        inputdata.append(inputdata_1)
#print(inputdata)

def compareList(data, inputdata):
   data.sort()
   inputdata.sort()
   if(data==inputdata):
      return "Equal"
   else:
      return "Non equal"

temp = [x for x in data if x not in inputdata]
print(temp)

print(compareList(data, inputdata))

if temp not in inputdata:
    for item in range(len(inputdata)):
        for z in range(len(temp)):
            if inputdata[item][0] == temp[z][0]:
                inputdata[item] = temp[z]
                print(inputdata)

