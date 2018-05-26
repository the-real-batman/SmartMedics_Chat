from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from autocorrect import spell

#################################################################

# Introduction and removal of stopwords
def correction(sentence,List):
	stop_words=set(stopwords.words('english'))
	word_tokens = word_tokenize(sentence)
	stop_words.remove('a')
	stop_words.remove('and')
	stop_words.remove('are')
	stop_words.remove('the')
	stop_words.remove('to')
	stop_words.remove('in')
	stop_words.remove('of')
	stop_words.remove('on')
	stop_words.remove('for')
	stop_words.remove('at')
	stop_words.remove('from')
	stop_words.remove('up')
	print("\n")
	words=[]
	filtered_sentence = [w for w in word_tokens if not w in stop_words]
	symbols=["," , ":" , ".","-"]
	sent=[w for w in filtered_sentence if not w in symbols]
	for w in sent:
	 	if w in List:
	 		words.append(w)
	 	else:
	 		try:
	 			words.append(str(float(w)))
	 		except:
	 			m=spell(w)
	 			words.append(m.lower())
	x=" ".join(words)
	return(x)

########################################################################################################

# Taking input
sentence=input("Describe your problem: ")
sentence=sentence.lower()
filepath = '123.csv'
master_list=[]
Sym_list=[]


#reading the file and storing the specialists, symptoms and weights in a list of lists
with open(filepath) as fp:  
   line = fp.readline()
   while line:
       stripped_line=line.strip()
       stripped_line = stripped_line.lower()
       strip_list=stripped_line.split(",")
       a=strip_list[0].split(" ")
       b=strip_list[1].split(" ")
       Sym_list.extend(a)
       Sym_list.extend(b)
       master_list.append(strip_list)
       line = fp.readline()

Sym_list=list(set(Sym_list))	
sentence=correction(sentence,Sym_list)

###############################################################################################

# Fifuring out the gender by matching the words to an existing dataset containing gender info
male=[]
female=[]
filename='MaleFemale.csv'
dataset=pd.read_csv(filename)
array=dataset.values
for i in array:
	male.append(i[0])
	female.append(i[1])

gender=''
for sex in word_tokenize(sentence):
	if sex in male:
		gender='Male'
		break
	elif sex in female:
		gender='Female'
		break

#####################################################################################

# Figuring out the presence of dominant and co-dominant keywords in the sentence
sum_list={}
dominant_key=''
psych_present=''
primary=['sex', 'cancer', 'eye','abortion']
primary_indices={} # dictionary used to store the keywords and their indices

for m in primary:
	if sentence.find(m)>=0:
		primary_indices[m]=sentence.find(m)

min_key=''

for key,value in primary_indices.items():
	if primary_indices[key]==min(primary_indices.values()):
		min_key=key

if min_key=='sex':
	if gender=='Female':
		if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
			dominant_key='gynaecologist'
			psych_present='psychiatrist'
			print('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
		else:
			dominant_key='gynaecologist'
			print('There is a high probability that you should consult a '+dominant_key)
	else:
		if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
			dominant_key='sexologist'
			psych_present='psychiatrist'
			print('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
		else:
			dominant_key='sexologist'
			print('There is a high probability that you should consult a '+dominant_key)

elif min_key=='cancer':
	dominant_key='oncologist'
	print('There is a high probability that you should consult a '+ dominant_key)
elif min_key=='eye':
	dominant_key='opthalmologist'
	print('There is a high probability that you should consult a '+ dominant_key)
elif 'abortion' in 'sentence':
	dominant_key='gynaecologist'
	print('There is a high probability that you should consult a '+ dominant_key)
else: # The following code runs if the dominant keywords are not present.
	for element in master_list:
		if sentence.find(element[1]) >= 0 :
			if not (element[0] in sum_list.keys()):
				sum_list[element[0]]=float(element[2])
			else:
				value=sum_list[element[0]]+float(element[2])
				sum_list[element[0]]=value
				
	total=0
	for value in sum_list.values():
		total = total + value
	for key in sum_list.keys():
		sum_list[key] = sum_list[key]*100/total
	for key,value in sum_list.items():
		print("The probability of going to {} is {} percent".format(key,value))