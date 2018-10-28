
import codecs
import sys
import math
import warnings
import re
import numpy as ny
from collections import defaultdict,Counter,OrderedDict


file = "address"   #argument file name
d1_letter = defaultdict #letters dictionary
d2_word = defaultdict   #word dictionary
count_letter = Counter()  #this dict is used for fast tallies and count of letters
count_words = Counter()   #this dict is used for fast tallies and count of words length
no_of_lines = 0     #records in file
total_characters = 0 #characters in file
invalid_characters =[] #invalid list of characters observed


with codecs.open( file, "r", "ISO-8859-1" ) as f: #opening a file using ISO-8859-1
     for line in f:                                #for loop of each line
         regex = re.sub(r'--', '  ',line)      #regex to replace all -- to two whitespaces
         modified_line = re.sub(r'[^a-z\-\']', ' ',regex, flags=re.IGNORECASE) #regex to replace all characters to single whitespace except letters(case insensitive), \' and \-
         modified_line = modified_line.lower() # converting all to lower case
         invalid_characters.extend(re.findall('[^a-zA-Z\-\' ]',regex)) #list of all invalid characters
         word = modified_line.split() #splitting all words from the line we got after above operations
         for w in word:               
            count_words[len(w)]+=1 #counting length of each word and equating it to Counter() ..which is a subcategory of dicts
         for letter in re.findall(r'[a-z]',modified_line):
             count_letter[letter]+=1 #counting occurrence of each letter and equating it to Counter()
         total_characters+=len(modified_line)
         no_of_lines+=1
         
         
d1_letter = {key:value for (key,value) in count_letter.items()} #dict comprehension for letters and their frequency of occurrence
d2_word = {key:value for (key,value) in count_words.items()} #dict comprehension for length of words and their frequency of occurrence

asc_letter_list = sorted([(key,value) for (key,value) in d1_letter.items()]) # List comprehension for ascending according to alphabets..a,b,c etc.
desc_list = sorted([(value,key) for (key,value) in d1_letter.items()],reverse=True) #List comprehension for descending the list
desc_letter_list = [(value,key) for (key,value) in desc_list] #List comprehension for descending according to frequency of occurrence of alphabets 
letter_freq_list = [value for (key,value) in d1_letter.items()] # list of only frequency (to calculate their sum in the end) 

asc_word_list = sorted([(key,value) for (key,value) in d2_word.items()]) # List comprehension for ascending according to length of word ..1,2,3 etc.
desc_word = sorted([(value,key) for (key,value) in d2_word.items()],reverse=True)
desc_word_list = [(value,key) for (key,value) in desc_word] # List comprehension for descending according to frequency of occurrence of words

# Assuming that each table we have to represent has dimesions 0f 5-across

dimension_letter = len(d1_letter) 
dimension_word = len(d2_word)
while(dimension_letter%5!=0):
    dimension_letter+=1           # calculating dimensions needed for letter table (5-across) if 26 items, which is an incomplete matrix,this gives 30 as dimension
while(dimension_word%5!=0):
    dimension_word+=1 # calculating dimensions needed for word table (5-across) 

dimension_zero =  dimension_letter-len(d1_letter)-2 #for filling numpy zeros and making it a complete matrix
dimension_letter = int(dimension_letter/5) #if 30 is the dimension this makes it 6 for 5-across table
dimension_word   = int(dimension_word/5) 

#using numpy arrays 

letter_array = ny.array(asc_letter_list,dtype = ('object,object')) #numpy array for letters and their frequency of occurrence
letter_array = ny.append(letter_array,ny.zeros((2,2), dtype=('object,object'))) # adjusting the matrix
letter_array = letter_array.reshape(5,dimension_letter) #reshaping it for 5-across table
letter_array = ny.transpose(letter_array) # transposing so rows becomes columns and columns becomes rows.


  #print function for tables
def print_table(table):
     for row in table:
         print("{:>15} {:>15} {:>15} {:>15} {:>25}".format(*row).replace(',','-').replace('[','').replace(']','  ').replace('(','   ').replace(')','   ').replace("'",'').replace('0- 0', ''))
    


print('    letter in ascending order- frequency of occurrence\n    ')
print_table(letter_array)


letter_array_desc = ny.array(desc_letter_list,dtype = ('object,object')) #numpy array for letters and their frequency of occurrence
letter_array_desc = ny.append(letter_array_desc,ny.zeros((dimension_zero,2), dtype=('object,object')))# adjusting the matrix
letter_array_desc = letter_array_desc.reshape(5,dimension_letter)#reshaping it for 5-across table
letter_array_desc = ny.transpose(letter_array_desc)# transposing so rows becomes columns and columns becomes rows.

print('\n    letter- frequency of occurrence in descending order\n    ')
print_table(letter_array_desc)


word_array = ny.array(asc_word_list,dtype = ('int,int')) #numpy array for words...1-word,2-word etc.
word_array = word_array.reshape(5,dimension_word)
word_array = ny.transpose(word_array)

print('\n    number of words - frequency of occurrence \n    ')
print('{:>16}'.format("len count"),'{:>20}'.format("len count"),'{:>18}'.format("len count"),'{:>19}'.format("len count"),'{:>20}'.format("len count"))
print_table(word_array)

list_rank = list(range(1,len(asc_word_list)+1)) #list of rank available
rank_table = ny.array(list_rank) #rank column
rank_table = rank_table.reshape(len(d2_word),1) # reshaping with respect to length of defaultdict of words

word_table_list = [key for (key,value) in desc_word_list] # list of keys only
word_table = ny.array(word_table_list) #word column 
word_table = word_table.reshape(len(d2_word),1)

frequency_table_list = [value for (key,value) in desc_word_list]
frequency_table = ny.array(frequency_table_list) #frequency column
frequency_table = frequency_table.reshape(len(d2_word),1)

length_freq = word_table*frequency_table # len*freq column
rank_freq = rank_table*frequency_table #rank*freq column

list_log_frequency = [round(math.log2(value),2) for (key,value) in desc_word_list] #list of log2 values of frequency
list_log_rank = [round(math.log2(items),2) for items in list_rank] #list of log2 values of rank

log_frequency_table = ny.array(list_log_frequency) #numpy array of log_frequency column
log_frequency_table = log_frequency_table.reshape(len(d2_word),1)
log_rank_table = ny.array(list_log_rank)
log_rank_table = log_rank_table.reshape(len(d2_word),1)
log_table = log_frequency_table/log_rank_table #dividing the columns
warnings.filterwarnings("ignore") # filtering warnings due to divide by zero warning
col1 = ny.append(rank_table,word_table,axis=1) 
col2 = ny.append(col1,frequency_table,axis=1)
col3 = ny.append(col2,length_freq,axis=1)
col4 = ny.append(col3,rank_freq,axis=1)  # final column after appending each
result = ny.append(col4,ny.array(log_table.round(decimals=2),dtype=object),axis=1)

print('\n\n')
print('{:>16}'.format("rank"),'{:>15}'.format("length"),'{:>12}'.format("freq"),'{:>16}'.format("length*freq"),'{:>14}'.format("rank*freq"),'{:>13}'.format("lgf/lgr"))

for col in result:
     print("{: >15}{: >15}{: >15}{: >15}{: >15}{: >15}".format(*col)) 

print('\n Total sum of frequency of words:',ny.sum(frequency_table))

print("\n Records read: \t\t  ",no_of_lines)
print(" Characters read: \t",total_characters)
print(" Characters counted: \t",sum(letter_freq_list))
print(" Words counted: \t ",ny.sum(frequency_table))
print(" Distinct characters: \t ",len(d1_letter))


print(" Invalid characters: \t ",list(OrderedDict.fromkeys(invalid_characters)) ) #unique values of invalid character list




import matplotlib.pyplot as plt
plt.plot(rank_table, frequency_table, 'ro')
