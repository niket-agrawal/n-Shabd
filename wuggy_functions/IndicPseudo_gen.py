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



def fill_freq(word_df,all_bigrams):
	w_df = word_df.copy()
	for i in range(len(w_df)):
		c1 = all_bigrams['Letter_n']==w_df.loc[i].Letter_n
		c2 = all_bigrams['n']==int(w_df.loc[i].n)
		c3 = all_bigrams['Letter_n+1']==w_df.loc[i]['Letter_n+1']
		df = all_bigrams[c1 & c2 & c3]
		#print(df.Freq.values[0])
		w_df.at[i, 'Freq'] = df.Freq.values[0] #same as #w_df['Freq'][i] = df.Freq.values[0]
		#print(w_df.loc[i].Freq)
	return w_df

def find_beam(word_df,all_bigrams):
	w_df = word_df.copy()
	fr_dev = 1
	flag = 0
	while(flag==0):
		#print("FR DEV = ",fr_dev)
		beam_size = []
		for i in range(len(w_df)):
			c1 = all_bigrams['Letter_n']==w_df.loc[i].Letter_n
			c2 = all_bigrams['n']==int(w_df.loc[i].n)
			c3 = all_bigrams['Letter_n+1']!=w_df.loc[i]['Letter_n+1']
			curr_fr = w_df.loc[i]['Freq'].item()
			max_dev = curr_fr+fr_dev
			min_dev = curr_fr-fr_dev
			c4 = (all_bigrams['Freq']<=max_dev) & (all_bigrams['Freq']>=min_dev)
			df = all_bigrams[c1 & c2 & c3 & c4]
			#print(df)
			beam_size.append(len(df))
		if(0 in beam_size[:-1] and fr_dev<=20):
			fr_dev += 1
		else:
			flag = 0
			w_df['beam'] = beam_size
			#print(word_df)
			#print(beam_size)
			#break
			return w_df, fr_dev


def find_options(word_df,all_bigrams,fr_dev):
	w_df = word_df.copy()
	temp = w_df[w_df.subs!=0]
	print(w_df)
	a = temp.beam.idxmax()
	wdf_row = w_df.iloc[a]
	########
	n = wdf_row.n
	#word_df.subs[word_df.n == n] = 0
	word_df.loc[(word_df.n==n),'subs']=0
	########
	c1 = all_bigrams['Letter_n']==wdf_row.Letter_n
	c2 = all_bigrams['n']==int(wdf_row.n)
	c3 = all_bigrams['Letter_n+1']!=wdf_row['Letter_n+1']
	curr_fr = wdf_row.Freq.item()
	max_dev = curr_fr+fr_dev
	min_dev = curr_fr-fr_dev
	c4 = (all_bigrams['Freq']<=max_dev) & (all_bigrams['Freq']>=min_dev)
	df = all_bigrams[c1 & c2 & c3 & c4]
	df = df.copy() #to suppress the warning
	fd = abs(df['Freq']-curr_fr)
	df['freq_diff'] = fd #warning because of this
	#df.loc[:,"freq_diff"] = fd #alternative 
	df = df.sort_values(by='freq_diff')
	df = df[0:5]
	a = zip(df['Letter_n+1'].values,[wdf_row.n]*len(df))
	a = list(a)
	return a

import anytree
from anytree import Node, RenderTree

def build_tree(word_df,all_bigrams,depth_max,node):
	w_df = word_df.copy()
	#w_df = orig_wdf.copy()
	lfs = node.leaves
	
	if(len(lfs)>20): 
		#print(lfs)
		for pre, fill, node in RenderTree(node):
			print("%s%s" % (pre, node.name))
		print("OVER")
		global pseudow_tree
		pseudow_tree = lfs
		return pseudow_tree
	for leaf in lfs:
		if (leaf.depth<3): #while
			l_name = leaf.name
			print("\tLOG - Current depth: ",leaf.depth)
			print("\tLOG - leaf name: ",l_name,end="")
			w_df = fill_freq(w_df,all_bigrams)
			w_df, deviation = find_beam(w_df, all_bigrams)
			opt = find_options(w_df,all_bigrams,deviation)
			print("---with options:",opt)
			#print(w_df)
			for item in opt:
				w_df.loc[(w_df.n==item[1]), 'Letter_n+1'] = item[0]
				tmp_pw = ''.join(w_df['Letter_n+1'].values[:-1])
				curr_n = Node(tmp_pw,parent=leaf)
				#curr_n = Node(w_df,parent=leaf)
				build_tree(w_df, all_bigrams, depth_max, node)
			#break
		#for pre, fill, node in RenderTree(node):
		#	print("%s%s" % (pre, node.name))
		#print("FINAL LENGTH: ",len(node.leaves))
	#for pre, fill, node in RenderTree(node):
	#	print("%s%s" % (pre, node.name))
	#print("FINAL LENGTH: ",len(node.root.leaves))
	

def generate_pseudo(word,lang,all_bigrams,leg,max_bigrams=5):
	word = "हरिहरन "
	print("LOG - Running for template word: ",word)
	
	word_df = create_bigrams(word,lang)
	word_df = pd.DataFrame([k.split(',')+[v] for k,v in word_df.items()])
	word_df.columns = ['Letter_n', 'n', 'max_n', 'Letter_n+1', 'Freq']
	pword_length = len(word_df)-1
	depth = substitute_stat(pword_length)
	print("LOG - This is",pword_length,"chracter long word. Max depth of tree (max. replacements): ",depth)
	
	all_bigrams = all_bigrams[all_bigrams['max_n']==pword_length]
	word_df['subs'] = [1]*(pword_length) + [0]
	tmp_pw = ''.join(word_df['Letter_n+1'].values[:-1])

	root = Node(tmp_pw)
	a = build_tree(word_df,all_bigrams,depth_max=3,node=root)
	print("Niket :",a)
	print(pseudow_tree)
	'''
	word_df = fill_freq(word_df,all_bigrams)
	print(word_df)
	word_df, deviation = find_beam(word_df,all_bigrams)
	print(word_df)
	max_psw = 10
	psw = []

	opt = find_options(word_df,all_bigrams,deviation)
	
	print(opt)

	i = 0
	deep = 0

	for pre, fill, node in RenderTree(root):
		print("%s%s" % (pre, node.name))
	
	while (len(psw)!=max_psw and deep<=depth):
		print("\n\n\n")
		toloop = opt[i]
		word_df.loc[(word_df.n==toloop[1]), 'Letter_n+1'] = toloop[0]

		word_df = fill_freq(word_df,all_bigrams)
		print(word_df)
		word_df, deviation = find_beam(word_df,all_bigrams)
		print(word_df)
		opt = find_options(word_df,all_bigrams,deviation)
		print(opt)
		i+=1
	'''
	#print(word_df)
	print("\n\n\n")