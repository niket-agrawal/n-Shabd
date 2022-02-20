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