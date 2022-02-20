def pseudowords_gen0(word,lang,max_bigrams=5):
	""" Generate pseudowords for the entered word
		Original
	"""
	print("LOG - Running for template word: ",word)
	word_bigram_dict = create_bigrams(word,lang)
	selected_bigs = []
	word_template_chain = []
	for key in word_bigram_dict.keys():
		word_bigram = key.split(",")
		word_template_chain.append(word_bigram)
		#to_search_word = word_bigram[0]+' '+word_bigram[1]+' '+word_bigram[2] #to think about (legacy)
		to_search_word = word_bigram[1]+' '+word_bigram[2]+' '+word_bigram[3]
		matched_bigrams={}
		#OPEN FILE (can be made faster if not opened file in a loop multiple times)
		big_chain = open("lang_resources/hi_bigrams.csv","r",encoding="utf-8")
		for big_line in big_chain:
			big_line = big_line.replace(',',' ')
			main_bigram = re.findall(r'\S+', big_line)
			#to_search_bigram = main_bigram[0]+' '+main_bigram[1]+' '+main_bigram[2] #to think about #legacy
			to_search_bigram = main_bigram[1]+' '+main_bigram[2]+' '+main_bigram[3]
			if(to_search_word==to_search_bigram and word_bigram[0]!=main_bigram[0]): #changed here for duplicate NWs
				matched_bigrams[main_bigram[0]] = int(main_bigram[4])
		big_chain.close()
		print(key)
		#CLOSE FILE
		sorted_mydict = sorted((value,key) for (key,value) in matched_bigrams.items())
		sorted_mydict = sorted(sorted_mydict, reverse = True)

		#### ***** ISSUE (b) ****** ###
		if(len(word_bigram_dict)==2):
			random.shuffle(sorted_mydict)
		###############################

		per_akshar_big = []
		for i in range(max_bigrams):
			if (len(sorted_mydict) > i):
				per_akshar_big.append(sorted_mydict[i][1])
				#print(sorted_mydict[i][1]+" ",end="")
				#f.write(sorted_mydict[i][1]+" ")
			else:
				break
		#f.write("\n")
		#print(per_akshar_big)
		selected_bigs.append(per_akshar_big)
		#print()

	##print("\t(a) bigram chain created for template word\n\t",word_template_chain)
	##print("\t(b)",wrd_replace,"bigrams for each letter selected acc to wuggy algo\n\t",selected_bigs)
	#print(selected_bigs)
	#print(word_template_chain)
	return selected_bigs, word_template_chain


def pseudowords_gen1(word,lang,all_bigrams,max_bigrams=5):
	""" Generate pseudowords for the entered word
		Imported dict
	"""
	print("LOG - Running for template word: ",word)
	word_bigram_dict = create_bigrams(word,lang)
	selected_bigs = []
	word_template_chain = []
	for key in word_bigram_dict.keys():
		word_bigram = key.split(",")
		word_template_chain.append(word_bigram)
		#to_search_word = word_bigram[0]+' '+word_bigram[1]+' '+word_bigram[2] #to think about (legacy)
		to_search_word = word_bigram[1]+','+word_bigram[2]+','+word_bigram[3]
		matched_bigrams={}
		for k, v in all_bigrams.items():
			a = k.split(",")
			to_search_bigram = a[1]+','+a[2]+','+a[3]
			if(to_search_word==to_search_bigram and word_bigram[0]!=a[0]): #changed here for duplicate NWs
				#print(a[0],all_bigrams[k])
				matched_bigrams[a[0]] = int(all_bigrams[k])
		print(key)

		sorted_mydict = sorted((value,key) for (key,value) in matched_bigrams.items())
		sorted_mydict = sorted(sorted_mydict, reverse = True)

		#### ***** ISSUE (b) ****** ###
		if(len(word_bigram_dict)==2):
			random.shuffle(sorted_mydict)
		###############################

		per_akshar_big = []
		for i in range(max_bigrams):
			if (len(sorted_mydict) > i):
				per_akshar_big.append(sorted_mydict[i][1])
				#print(sorted_mydict[i][1]+" ",end="")
				#f.write(sorted_mydict[i][1]+" ")
			else:
				break
		#f.write("\n")
		#print(per_akshar_big)
		selected_bigs.append(per_akshar_big)
		#print()

	##print("\t(a) bigram chain created for template word\n\t",word_template_chain)
	##print("\t(b)",wrd_replace,"bigrams for each letter selected acc to wuggy algo\n\t",selected_bigs)
	return selected_bigs, word_template_chain


def pseudowords_gen2(word,lang,all_bigrams,max_bigrams=5):
	""" Generate pseudowords for the entered word
		Imported df
	"""
	print("LOG - Running for template word: ",word)
	word_bigram_dict = create_bigrams(word,lang)
	selected_bigs = []
	word_template_chain = []
	for key in word_bigram_dict.keys():
		word_bigram = key.split(",")
		word_template_chain.append(word_bigram)
		#to_search_word = word_bigram[0]+' '+word_bigram[1]+' '+word_bigram[2] #to think about (legacy)
		to_search_word = word_bigram[1]+','+word_bigram[2]+','+word_bigram[3]
		df = all_bigrams [(all_bigrams['Letter_n+1']==word_bigram[3]) & (all_bigrams['n']==int(word_bigram[1])) & (all_bigrams['max_n']==int(word_bigram[2]))]
		df = df.sort_values(by='Freq', ascending=False)
		#### ***** ISSUE (b) ****** ###
		#if(len(word_bigram_dict)==2):
		#	df = df.sample(frac=1)
		###############################
		df = df[0:5]
		print(df)
		print(key)
		'''
		matched_bigrams={}
		for k, v in all_bigrams.items():
			a = k.split(",")
			to_search_bigram = a[1]+','+a[2]+','+a[3]
			if(to_search_word==to_search_bigram and word_bigram[0]!=a[0]): #changed here for duplicate NWs
				#print(a[0],all_bigrams[k])
				matched_bigrams[a[0]] = int(all_bigrams[k])
		print(key)

		sorted_mydict = sorted((value,key) for (key,value) in matched_bigrams.items())
		sorted_mydict = sorted(sorted_mydict, reverse = True)

		per_akshar_big = []
		for i in range(max_bigrams):
			if (len(sorted_mydict) > i):
				per_akshar_big.append(sorted_mydict[i][1])
				#print(sorted_mydict[i][1]+" ",end="")
				#f.write(sorted_mydict[i][1]+" ")
			else:
				break
		#f.write("\n")
		#print(per_akshar_big)
		selected_bigs.append(per_akshar_big)
		#print()

	##print("\t(a) bigram chain created for template word\n\t",word_template_chain)
	##print("\t(b)",wrd_replace,"bigrams for each letter selected acc to wuggy algo\n\t",selected_bigs)
	return selected_bigs, word_template_chain
	'''


