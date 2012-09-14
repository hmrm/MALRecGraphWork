import sys

lines = open(sys.argv[1]).readlines()

found = True

for line in lines:
    if line[0] == "h": #http:// ie
        if not found:
            print "1"
        parts = line.strip().split("/")
        print parts[4],
        found = False
    else:
        print line.strip()
        found = True

if not found:
    print "1"
