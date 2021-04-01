#imports
import os
import hashlib
import datetime
from os.path import expanduser
#store unhashable directories in a list to ignore
hashFile = open("HashData.csv", "r", encoding ='utf8')
keep = {}
#First Trial: recursively list all the files/folders that we want to hash
#Start at "/"
for root, dirpath, file  in os.walk("/"):
	start = root[0:8] #leftover from comparing dirpath, avoid a long dirpath that happens to also contain a bad name
	target = 0 #this variable acts like a switch that turns "on" if the root starts with one of our unhashable directories
	if "/dev" in start:
		target = 1
	elif "/proc" in start:
		target = 1
	elif "/run" in start:
		target = 1
	elif "/sys" in start:
		target = 1
	elif "/tmp" in start:
		target = 1
	elif "/var/lib" in start:
		target = 1
	elif "/var/run" in start:
		target = 1
	elif "/usr" in start:
		target = 1
	elif "/var/ossec/queue" in root:
		target = 1
	elif "/var/spool" in root:
		target = 1
	elif target == 0:
	#	keep.append(root)
		for name in file:
			fullName = os.path.join(root, name) #step 1 complete
			#keep.append(fullName) 
			f = open(fullName, "rb")
			bytes = f.read()
			hash = hashlib.sha256(bytes).hexdigest()
		#	print(hash) step 2 complete
			timeStamp = datetime.datetime.now()
			timeStamp = str(timeStamp)
#			print(timeStamp)
# Leave out initial write for all future versions, now need to compare
		#	hashFile.write(fullName+ "," + hash + "," + timeStamp+ "\n")
			keep[fullName] = hash
#Part 4 Logic: We have a dictionary of the newest hashes, in the keep dictionary
#Now make dictionaries for modified files, new files, removed files
#File Info contains info from the previous .csv file
modifiedFiles = {}
newFiles = {}
removedFiles = {}
fileInfo = {}
for line in hashFile:
	line = line.split(",")
	fileName = line[0]
	fileHash = line[1]
	fileInfo[fileName] = fileHash #fills based on old csv file
for key in keep:
#Logic: go through new files, if file name in the list of old files, check the hashes to see if the file was modified 
	if key in fileInfo:
		newHash = keep.get(key)
#		print(newHash)
		oldHash = fileInfo.get(key)
#		print(oldHash)
		if newHash != oldHash:
			modifiedFiles[key] = newHash
	else: #if it wasn't in the dict of old files then it's a new file
		hash = keep.get(key)
		newFiles[key] = hash
for key in fileInfo: #now go backwards to find removed files
	if key not in keep: #look at old file names and compare to dict of new file names
		hash = fileInfo.get(key) #if it isn't in the new dictionary, the file was removed
		removedFiles[key] = hash
	else:
		continue
print("Modified Files:") #create print output
for key, value in modifiedFiles.items():
	print("File Name:" + key)
	print("Hash:" + value)
print("New Files:")
for key, value in newFiles.items():
	print("File Name:" + key)
	print("Hash:" + value) 
print("Removed Files:")
for key, value in removedFiles.items():
	print("File Name:" + key)
	print("Hash:" + value) 
hashFile.close()
newHF = open("HashData.csv", "w", encoding = 'utf8')
timeStamp = datetime.datetime.now()
timeStamp = str(timeStamp)
for key, value in fileInfo.items():
	newHF.write(key + "," + value + "," + timeStamp + "\n")
newHF.close() #write and create the newest hash file
