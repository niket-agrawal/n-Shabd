import unicodedata
import re
import pandas as pd

def create_bigrams(word,lang):
	""" Convert shabd(word) to bigrams alongwith its frequency
	"""
	if lang=="hi": language="DEVANAGARI"
	elif lang=="te": language="TELUGU"
	
	bi_chain={}
	index=0
	string = word.strip()
	chars = [s for s in string]
	akshars=[]

	for c in chars:
		temp=unicodedata.name(c)
		akshar=temp.find(language+' LETTER',0)
		if akshar!=-1:
			akshars.append(c)
			index=index+1
		else:
			if index!=0:
				akshars[index-1]=akshars[index-1]+c
	akshars.insert(0,'-') #Older(legacy)
	akshars.append('-')
	len_akshars = len(akshars)-1
	for i in range(len_akshars):
		#chain = akshars[i] +','+ str(i+1) +','+ str(len_akshars+1) +','+ akshars[i+1] #Older(legacy)
		#chain = akshars[i] +','+ str(i+1) +','+ str(len_akshars) +','+ akshars[i+1] #Older(legacy2)
		chain = akshars[i] +','+ str(i) +','+ str(len_akshars-1) +','+ akshars[i+1]
		if chain in bi_chain:
			bi_chain[chain]+=1
		else:
			bi_chain[chain]=1
	return bi_chain
#a = create_bigrams("प्यारा")
#print(a)

def bigram_language_df(lang):
	bigram_df = pd.read_csv('lang_resources/'+lang+'_bigrams.csv', sep=',')
	return bigram_df

def bigram_language(lang):
	all_bigrams={}
	big_chain = open('lang_resources/'+lang+'_bigrams.csv','r',encoding='utf-8-sig')
	for big_line in big_chain:
		bi = big_line.strip().split(',')
		all_bigrams[bi[0]+','+bi[1]+','+bi[2]+','+bi[3]] = bi[4]
	return all_bigrams

def join_dict(big_dict, small_dict):
	""" Merges two dictionary, 1 big and 1 small, and returns single big dictionary
	"""
	for key in small_dict:
		if key in big_dict:
			big_dict[key] = int(big_dict[key])+int(small_dict[key])
		else:
			big_dict[key] = small_dict[key]
	return big_dict


# Python3 program to print all combinations of size
# k of elements in set 1..n
def makeCombiUtil(n, left, k):
    # Pushing this vector to a vector of vector
    if (k == 0):
        ans.append(tmp)
        a = []
        for i in range(len(tmp)):
            a.append(tmp[i])
        all_combs.append(a)
        return
    # i iterates from left to n. First time
    # left will be 1
    for i in range(left, n + 1):
        tmp.append(i)
        makeCombiUtil(n, i + 1, k - 1)
        # Popping out last inserted element
        # from the vector
        tmp.pop()

def makeCombi(n, k):
    makeCombiUtil(n, 1, k)
    return ans

def func1(n,k):
    global ans
    ans = []
    global tmp
    tmp= []
    global all_combs
    all_combs = []
    ans = makeCombi(n, k)
    return(all_combs)
# This code is contributed by divyeshrabadiya07.
'''
a = list(range(2,21))
for i in a:
    for j in range(1,int(i/2)+1):
        if(j/i>=0.333 and j/i<=0.5):
            print(j,"out of",i,"aksharas changed, difference of",j/i,"%")
            how_many = j
            break
    combnx = func1(i,how_many)
    print(i,how_many,len(combnx))
'''
def substitute_stat(n):
    #n = int(input("Please enter word length:"))
    for j in range(1,int(n/2)+1):
        if(j/n>=0.333 and j/n<=0.5):
            #print(j,"out of",n,"aksharas changed, difference of",j/n,"%")
            how_many = j
            break
    combx = func1(n,how_many)
    #print(len(combx),"unique combinations can be made")
    #print(n,how_many,len(combx),"\n",combx)
    return how_many
#substitute_stat(10)

#a = list(range(2,21))
#print(a)
#for i in a:
#    substitute_stat(i)

def find_weakest_link(all_bigrams,word_df):
	pwr = 1
	flag = 1
	while flag!=0:
		frq = [[],[]]
		print("PASSSSSS with pwr = ",pwr)
		for item in word_df.iterrows():
			item1 = item[1]
			at0 = item1.Letter_n
			at1 = item1.n
			#at3 = item1['Letter_n+1']
			#df = all_bigrams.copy()		
			df = all_bigrams[(all_bigrams['Letter_n']==at0) & (all_bigrams['n']==int(at1))]
			df = df.sort_values(by='Freq', ascending=False)
			### select freq ##############################
			fr = df[df['Letter_n+1']==item1['Letter_n+1']]['Freq']
			if(fr.empty): fr=1
			fr = int(fr)
			#frq_deviation = pow(2,pwr)
			frq_deviation = pwr
			cutoff_fr_max = fr+frq_deviation
			cutoff_fr_min = fr-frq_deviation
			#print(cutoff_fr_min,fr,cutoff_fr_max)
			##############################################
			#print(at0,at1,at3,fr)
			frq[0].append(fr)
			df = df[(df['Freq']>=cutoff_fr_min) & (df['Freq']<=cutoff_fr_max) & (df['Letter_n+1']!=item1['Letter_n+1'])]
			df['freq_diff'] = abs(df['Freq']-fr)
			df = df.sort_values(by='freq_diff')
			#print(df)
			frq[1].append(len(df))

		word_df['Freq'] = frq[0]
		word_df['deviation_n'] = frq[1]
		#word_bigrams_df = word_bigrams_df.iloc[:-1 , :]
		#print(word_bigrams_df)
		if(0 in word_df['deviation_n'].values[:-1] and (pwr<=20)):
			pwr = pwr+1
		else:
			flag = 0
	word_df = word_df.iloc[:-1 , :]
	
	#print(word_bigrams_df)
	#combx = substitute_stat(pword_length)
	priority = word_df.n.astype(int).values
	#print(priority)
	# newc = []
	# for i in range(len(priority)-1):
	# 	for j in range(i+1,len(priority)):
	# 		newc.append((priority[i],priority[j]))
	# print(newc)
	weakest = priority[0]
	return priority, pwr

def recursive_replace(word_orig, word_df, n):
	word_df = word_df.sort_values(by=['tobe_replaced','deviation_n'], ascending=(False,False)).reset_index(drop=True)
	print(word_orig)
	print(word_df)
	count0 = len([word_df['tobe_replaced'] == 0])
	item_to_rep = word_df.loc[0]
	if count0==n+1:
		return word_df
	else:
		print(item_to_rep)
		return 0
		print("Niket")
		n=n-1
		recursive_replace(word_orig, word_df, n)
	

def generate_pseudo(word,lang,all_bigrams,leg,max_bigrams=5):
	print("LOG - Running for template word: ",word)
	print("LOG - Legacy version running: ",leg)
	#word = input("Enter template:")
	word = "हरिहरन "
	word_bigram_dict = create_bigrams(word,lang)
	word_bigrams_df = pd.DataFrame([k.split(',')+[v] for k,v in word_bigram_dict.items()])
	word_bigrams_df.columns = ['Letter_n', 'n', 'max_n', 'Letter_n+1', 'Freq']
	pword_length = len(word_bigrams_df)-1
	all_bigrams = all_bigrams[all_bigrams['max_n']==pword_length]
	#print(all_bigrams)
	word_orig = word_bigrams_df.copy()
	weak, pwr = find_weakest_link(all_bigrams,word_bigrams_df)
	print("   LOG - Weakest link is: ",weak)
	n = substitute_stat(pword_length)
	print("   LOG - No of replacements: ",n)
	word_bigrams_df['tobe_replaced'] = [1]*(pword_length) + [0]
	#print(word_bigrams_df)
	print("TESTING")
	#print(word_bigrams_df)
	#print(word_bigrams_df.loc[0])
	a = recursive_replace(word_orig,word_bigrams_df,n)
	print(a)


	print("\n\n\n\nFORGET IT")
	for link in weak:
		tempdf = word_bigrams_df[word_bigrams_df['n']==str(link)]
		at0 = tempdf.Letter_n.values[0]
		at1 = tempdf.n.values[0]
		at4 = tempdf.Freq.values[0]
		at3 = tempdf['Letter_n+1'].values[0]
		#print(at0,at1)
		df = all_bigrams[(all_bigrams['Letter_n']==at0) & (all_bigrams['n']==int(at1))]
		df = df.sort_values(by='Freq', ascending=False)
		frq_deviation = pwr
		fr = at4
		cutoff_fr_max = fr+frq_deviation
		cutoff_fr_min = fr-frq_deviation
		df = df[(df['Freq']>=cutoff_fr_min) & (df['Freq']<=cutoff_fr_max) & (df['Letter_n+1']!=at3)]
		df['freq_diff'] = abs(df['Freq']-fr)
		df = df.sort_values(by='freq_diff')
		df = df[0:5]
		print(df)
			


	



def pseudowords_gen(word,lang,all_bigrams,leg,max_bigrams=5):
	""" Generate pseudowords for the entered word
		Imported dict
	"""
	#max_bigrams = 20
	word = input("Enter template:")
	print("LOG - Running for template word: ",word)
	print("LOG - Legacy version running: ",leg)
	word_bigram_dict = create_bigrams(word,lang)
	word_bigrams_df = pd.DataFrame([k.split(',')+[v] for k,v in word_bigram_dict.items()])
	word_bigrams_df.columns = ['Letter_n', 'n', 'max_n', 'Letter_n+1', 'Freq']
	#print(all_bigrams)
	#print(word_bigrams_df)
	word_length = len(word_bigrams_df)-1
	max_pseudow = max_bigrams*word_length
	pwr = 1
	flag = 1
	print("Max pseudo = ",max_pseudow)
	while flag!=0:
		print("\n\n####PASS with pwr=####",pwr)
		
		pseudo_bigrams = pd.DataFrame()
		for item in word_bigrams_df.iterrows():
			item1 = item[1]
			at0=item1.Letter_n
			at1=item1.n
			at2=item1.max_n
			df = all_bigrams[(all_bigrams['Letter_n']==at0) & (all_bigrams['n']==int(at1)) & (all_bigrams['max_n']==int(at2))]
			df = df.sort_values(by='Freq', ascending=False)
			### select freq ##############################
			fr = df[df['Letter_n+1']==item1['Letter_n+1']]['Freq']
			if(fr.empty): fr=1
			fr = int(fr)
			#frq_deviation = pow(2,pwr)
			frq_deviation = pwr
			cutoff_fr_max = fr+frq_deviation
			cutoff_fr_min = fr-frq_deviation
			print(cutoff_fr_min,fr,cutoff_fr_max)
			##############################################
			if(leg==1):
				df = df[df['Letter_n+1']!=item1['Letter_n+1']]
				df = df[0:5]
				pseudo_bigrams = pseudo_bigrams.append(df)
			elif(leg==2):
				df = df[(df['Freq']>=cutoff_fr_min) & (df['Freq']<=cutoff_fr_max) & (df['Letter_n+1']!=item1['Letter_n+1'])]
				#df = df[(df['Freq']>=cutoff_fr_min) & (df['Freq']<=cutoff_fr_max)]
				df['freq_diff'] = abs(df['Freq']-fr)
				df = df.sort_values(by='freq_diff')
				df = df[0:5]
				pseudo_bigrams = pseudo_bigrams.append(df)
				pseudo_bigrams = pseudo_bigrams.sort_values(by='freq_diff')

			print(len(df))
		
		if(pwr==20): flag=0;
		#if (argument passed to match matras, subsyllabic structure)
			# filter again
			# df = df
		if(len(pseudo_bigrams)>=max_pseudow and leg==2): flag=0
		elif(leg==2): pwr+=1
		elif(leg==1): flag=0

		if(leg==2): pseudo_bigrams = pseudo_bigrams[0:20]
		
	return pseudo_bigrams, word_bigrams_df