For this program, I initially created the first file with the format:
filename, hash, timestamp
This creates the baseline of hashfiles to be read into a dictionary
From there, you can read in this (or whatever becomes the most recent file), 
run a SHA256 hash function on the file system (avoiding "unhashable" paths).
I stored these newest filenames and hashes in a dictionary.
Then, using the baseline dictionary and the new dictionary, comparisons can be made:
First: look for modified files:
	This lies on the assumption that the file exists in both the new and old dictionaries
	If the hashes are different, the file was modified and we add the file info to our modified dictionary
Then: look for new files:
	This lies on the assumption that the file exists in the new dictionary, but not the old one.
	If this is the case, we add the file info to the new file dictionary
Finally: look for removed files:
	This lies on the assumption that the file exists in the old dictionary, but not the new one
	If this is the case, we add the file info to the old file dictionary
At the end of all this,print the three dictionaries and write the newest dictionary to the hashfile to create our newest version of the hashfile

