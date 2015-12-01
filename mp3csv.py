"""mp3csv.py

Extracts the ID3 tags from MP3s contained within a directory structure and
writes them to a CSV file. Uses EasyID3 from the mutagen Python module.

Usage: python mp3csv.py path output.csv
"""

import os
from sys import argv
try:
    from mutagen.easyid3 import EasyID3
except ImportError:
    print "Could not import mutagen.easyid3"
    print "You may need to install the mutagen Python module"
    exit(1)

# the ID3 tag fields to extract
# N.B. can only use ones compatible with mutagen's EasyMP3
fields = ['artist', 'title', 'composer', 'album']

try:
    dir = argv[1]
    csv = argv[2]
except IndexError:
    print "Usage: python mp3csv.py path output.csv"
    exit(1)

if os.path.isfile(csv):
    print "CSV file already exists. Please delete and run again"
    exit(1)

f = open(csv, 'w')

# walk the directory structure
for root, dirs, files in os.walk(dir):
    for file in files:
        if file.endswith(".mp3"):
            # build up a whole line then write to file to avoid extra spaces
            # include path and filename with csv delimiters
            # use unicode() to avoid mixing str and unicode types
            # (tags are unicode but path could be str)
            line = unicode('"' + os.path.join(root, file) + '",', 'utf-8')
            # create an object for this MP3 file's ID3 tag
            tag = EasyID3(os.path.join(root, file))
            # for each tag field from the list above
            for field in fields:
                line += '"'
                # must check if it's there to avoid error
                if field in tag:
                    line += tag[field][0]
                line += '"'
                # if this is the last field in the list
                if field == fields[-1]:
                    line += '\n'
                    f.write(line.encode('utf-8'))
                # if there are still fields to go in this row
                else:
                    line += ','

f.close()
