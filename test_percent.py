from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from autocorrect import spell
import csv

#################################################################

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

def prediction(sentence):
	sentence=sentence.lower()
	filepath = 'example2.csv'
	symptom_list=[]
	keyword_list=[]
	disease_list=[]
	psych_list=[]


	with open(filepath) as fp:  
	   line = fp.readline()
	   while line:
	       stripped_line=line.strip()
	       stripped_line = stripped_line.lower()
	       strip_list=stripped_line.split(",")
	       a=strip_list[0].split(" ")
	       b=strip_list[1].split(" ")
	       keyword_list.extend(a)
	       keyword_list.extend(b)
	       symptom_list.append(strip_list)
	       line = fp.readline()

	with open('DiseasesData.csv') as fp:
		line = fp.readline()
		while line:
			stripped_line=line.strip()
			stripped_line=stripped_line.lower()
			strip_list=stripped_line.split(",")
			a=strip_list[0].split(" ")
			b=strip_list[1].split(" ")
			keyword_list.extend(a)
			keyword_list.extend(b)
			disease_list.append(strip_list)
			line=fp.readline()

	with open('psychiatrist.csv') as fp:
		line = fp.readline()
		while line:
			stripped_line=line.strip()
			stripped_line=stripped_line.lower()
			strip_list=stripped_line.split(",")
			a=strip_list[0].split(" ")
			b=strip_list[1].split(" ")
			keyword_list.extend(a)
			keyword_list.extend(b)
			psych_list.append(strip_list)
			line=fp.readline()

	keyword_list=list(set(keyword_list))	
	sentence=correction(sentence,keyword_list)


	###############################################################################################

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
			##print(sex)
			gender='Male'
			break
		elif sex in female:
			##print(sex)
			gender='Female'
			break

	#####################################################################################

	symptom_dict={}
	dominant_key=''
	psych_present=''
	primary=['sex', 'cancer','abortion']
	primary_indices={}
	flag=0
	disease=""
	specialist=""
	for element in disease_list:
		if sentence.find(element[1])>=0:
			flag=1
			disease=element[1]
			specialist=element[0]
			break
	if flag==1:
		return("You should consult a {}".format(specialist))

	elif flag==0:	
		for m in primary:
			if sentence.find(m)>=0:
				primary_indices[m]=sentence.find(m)

		min_key=''

		for key,value in primary_indices.items():
			if primary_indices[key]==min(primary_indices.values()):
				min_key=key

		if min_key=='sex':
			if gender=='Female' or sentence.find('pregnancy')>=0 or sentence.find('pregnant')>=0 or sentence.find('period')>=0 :
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
					dominant_key='gynaecologist'
					psych_present='psychiatrist'
					return('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
				else:
					dominant_key='gynaecologist'
					return('There is a high probability that you should consult a '+dominant_key)
			else:
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
					dominant_key='sexologist'
					psych_present='psychiatrist'
					return('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
				elif sentence.find('period')>=0 or sentence.find('abortion')>=0:
					dominant_key='gynaecologist'
					return('There is a high probability that you should consult a '+dominant_key)
				else:
					dominant_key='sexologist'
					return('There is a high probability that you should consult a '+dominant_key)

		elif min_key=='cancer':
			dominant_key='oncologist'
			return('There is a high probability that you should consult a '+ dominant_key)
		elif sentence.find('abortion')>=0 or sentence.find('period')>=0 :
			if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
				dominant_key='gynaecologist'
				psych_present='psychiatrist'
				return('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
			else:
				dominant_key='gynaecologist'
				return('There is a high probability that you should consult a '+dominant_key)


		else:
			for element in symptom_list:
				if sentence.find(element[1]) >= 0 :
					if not (element[0] in symptom_dict.keys()):
						symptom_dict[element[0]]=float(element[2])
					else:
						value=symptom_dict[element[0]]+float(element[2])
						symptom_dict[element[0]]=value
			total=0
			for value in symptom_dict.values():
				total = total + value
			for key in symptom_dict.keys():
				symptom_dict[key] = symptom_dict[key]*100/total

			sortedDict={}
			new_list=sorted(symptom_dict.items(), key = lambda t: t[1], reverse = True)
			print_list=[]
			flag1=0
			for item in new_list:
				flag1=flag1+1
				if flag1 < 3:
					print_list.append(item[0])
			if print_list!=[]:
				return('Based on the symptoms you should consult a '+' and '.join(print_list))	
			if symptom_dict=={}:
				for element in psych_list:
					if sentence.find(element[1])>=0:
						return('You should visit a psychiatrist')


if __name__ == "__main__":
	m=[]
	with open('probs.csv') as fp:  
	   line = fp.readline()
	   while line:
	       stripped_line=line.strip()
	       stripped_line = stripped_line.lower()
	       m.append(stripped_line)
	       line = fp.readline()

	

	file1 = open("myfile.txt","w")

	for element in m:
		print(element)
		try:
			a=prediction(element)
			string= element + " , " + a + " \n"
			file1.write(string)
		except:
			string= element + " , " + " \n"
			file1.write(string)

	file1.close()





