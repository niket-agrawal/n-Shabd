import os, sys, inspect, csv
from IndicPseudo_gen import create_bigrams, join_dict
import argparse

parser = argparse.ArgumentParser(description="Find bigrams of a given language if word list is the input")
h1= "input word list of any particular language to create bigram file"
h2= "name of the language, bigram file for that language will look like language_bigrams.csv"
h3= "encoding format of the input word list file, eg utf-8, utf-8-sig"
parser.add_argument("-w", "--word_list", default="hi_words_used_to_gen_bigrams.txt", metavar="", help=h1)
parser.add_argument("-l", "--language", default="hi", choices=['hi','en','ur','te'], metavar="", help=h2)
parser.add_argument("-e", "--encoding", default="utf-8", choices=['utf-8','utf-8-sig'], metavar="", help=h3)
args = parser.parse_args()

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
lang_path = parentdir+"\\lang_resources\\"

f_name = lang_path + args.word_list
output_path = lang_path + args.language + "_bigrams.csv"

x={}
cnt_line = 0
with open(f_name, encoding=args.encoding) as wf1:
	for w1 in wf1:
		w1 = w1.strip()
		small_dict = create_bigrams(w1, args.language)
		x = join_dict(x,small_dict)
		cnt_line+=1
		print("Total words read = ", cnt_line,"\r",end="",flush=True)
print('\n\nSUCCESS - Bigrams generated, length =',len(x))

print('\nNow saving csv file (utf-8-sig) : ',output_path)
with open(output_path,'w',encoding='utf-8-sig',newline='') as f:
    #w = csv.writer(sys.stderr) # to check
    w = csv.writer(f)
    w.writerow(['Letter_n', 'n', 'max_n', 'Letter_n+1', 'Freq'])
    for key, value in x.items():
    	row = key+","+str(value)
    	w.writerow(row.split(","))
    #w.writerows(x.items())
print('\nSUCCESS - DONE, you can exit')