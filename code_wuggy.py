import re
import sys
import os
import random
import codecs
import operator
## -*- coding: utf-8 -*-
#big_chain = open("dat6_bigram_chains.txt","r",encoding="utf-8")
template_raw = open("inp1_template.txt","r",encoding="utf-8")
input_word = ""

#### Descriptive Stats #####
import Levenshtein
import numpy as np
import pandas as pd
import itertools
f_name = "lang_resources/hi_all-words.csv"

x = []
with open(f_name, encoding='utf-8') as wf1:
	for w1 in wf1:
		w1 = w1.split(",")
		w1 = w1[0]
		w1 = w1.strip()
		x.append(w1)


#############################



sys.path.append("D:/IITK Temp/NonWords_Vivek/custom-packages")
sys.path.append("D:/IITK Temp/Wuggy/wuggy_base_vtest/wuggy_functions")
from IndicPseudo_gen import create_bigrams, bigram_language, generate_pseudo, bigram_language_df
import timing

input_words = [input_word.splitlines()[0] for input_word in template_raw]


f=codecs.open("op1_non_words2.csv","w","UTF-8-sig")
df = bigram_language_df("hi")
#df = bigram_language("hi")
wrd_replace = 5

#for input_word in input_words:
for i in range(1):
	input_word = "स्वागतम्"
	all_non_words = []
	legacy_code = 3
	#1 for original version (one at a time replacement) (BASED ON HIGHEST FREQUENCY)
	#1+ for better original version (improvement in the idea that first akshar will change somehow)
	#2 for current wuggylike version (one at a time replacement but not based on highest freq, BASED ON TRANSITION FREQ)
	#3 for multiple replacements 
	selected_bigs, word_template_chain = generate_pseudo(input_word, "hi", df,legacy_code,wrd_replace)
	print(selected_bigs)
	print(word_template_chain)
	
	for item in selected_bigs.iterrows():
		item1 = item[1]
		wtc = word_template_chain.copy()
		wtc.loc[wtc.n==str(item1.n), 'Letter_n+1'] = item1['Letter_n+1']
		nw = wtc['Letter_n+1'].tolist()
		nw = nw[:-1]
		#nw = ''.join(nw)
		a = ""
		for i in nw: a=a+i
		#print(a,end=",")
		all_non_words.append(a)
	print()
	
	'''
	#selected_bigs, word_template_chain = pseudowords_gen2(input_word, "hi",wrd_replace)	
	temp_split = [i[0] for i in word_template_chain] + ['']
	##print("\t(c) template word temporarily split for non-words generation\n\t",temp_split)

	j=1
	all_non_words = []
	len_template = len(temp_split)
	for item in selected_bigs:
		nw_temp = []
		len_bigs = len(item)
		for i in range(len_bigs):
			temp = temp_split.copy()
			if(j<len_template):
				temp[j] = item[i]
			elif(j==len_template):
				temp.append(item[i])
			non_wrd = temp
			non_wrd = ''.join(non_wrd[1:])
			nw_temp.append(non_wrd)
		j=j+1
		all_non_words.append(nw_temp)
		print(nw_temp)
	#print("\t(d) Non-word list created\n\t",all_non_words)
	all_non_words = [item for sublist in all_non_words for item in sublist] #flatten list of list
	
	
	#df = pd.DataFrame()
	'''
	
	for nw in all_non_words:
		row = []
		with open(f_name, encoding='utf-8') as wf2:
			row = [Levenshtein.distance(w2.split(",")[0].strip(),nw) for w2 in wf2]
			row.sort()
			row = row[0:20] #OLD 20
			old20 = sum(row)/len(row)
			#print(row)
		wf2.close()
		#df[nw] = row
		
		f.write(input_word+","+nw+","+str(old20))
		print(input_word+","+nw+","+str(old20))
		f.write("\n")
	
	#df.index = x
	#print(df)

	#for col in df.columns:
	#	subs = df[col]
	#	subs = subs.sort_values(ascending=True)
	#	subs = subs.iloc[0:20]
	#	print(subs)