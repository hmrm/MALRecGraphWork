from bs4 import BeautifulSoup
import sys
import codecs

infiles = sys.stdin.readlines()
outdir = sys.argv[1]

for infile in infiles:
    print infile
    soup = BeautifulSoup(open(infile[:-1]).read())
    outfile = codecs.open(outdir + "/" + infile[:-1] + "-parsed", "w", "utf-8")

    for text in soup.find_all("strong"):
        try:
            if not text.parent.parent["class"] == "spaceit":
                outfile.write(text.text)
                outfile.write("\n")
        except KeyError:
            outfile.write(text.parent["href"])
            outfile.write("\n")
