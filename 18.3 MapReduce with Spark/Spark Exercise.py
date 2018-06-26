import pyspark
import matplotlib.pyplot as plt
import numpy as np
plt.figure(figsize=(16,10))

sc=pyspark.SparkContext()

"""Loading in stop words into a python list and julius caezar.txt into an RDD."""
with open(r"C:\Users\Lukas Buteliauskas\Desktop\Springboard Projects\18.3 MapReduce with Spark\sparklect\english.stop.txt", "r") as file:
    stop_words=file.readlines()

stop_words=[x.strip() for x in stop_words]

juliusrdd=sc.textFile(r"C:\Users\Lukas Buteliauskas\Desktop\Springboard Projects\18.3 MapReduce with Spark\sparklect\shakes\juliuscaesar.txt")

"""How many words does Julius Caesar have? Hint: use flatMap()."""

julius_words=juliusrdd.flatMap(lambda x: x.split()).cache()
print("Julius Caezar has ", len(julius_words.collect()), " words\n")

"""Now print the first 20 words of Julius Caesar as a Python list."""

print("First 20 Julius Caezar words:\n", julius_words.take(20),"\n")

"""Now print the first 20 words of Julius Caesar, after removing all the stopwords. Hint: use filter()."""

filtered_julius_words=julius_words.filter(lambda word: word.lower() not in stop_words)
filtered_julius_words=filtered_julius_words.filter(lambda word: word is not '"').cache()
print("First 20 Julius Caezar words (with stop words removed):\n", filtered_julius_words.take(20), "\n")

"""Top 20 most common words"""
most_common_words=filtered_julius_words.map(lambda x: (x,1)).reduceByKey(lambda x,y: x+y)
most_common_words_20=most_common_words.takeOrdered(20, key=lambda x: -x[1])
print("20 Most common Julius Caezar words:\n", most_common_words_20,"\n")

"""Bar chart of 20 most common words"""

plt.bar(x=[x for x in range(20)], height=np.array(most_common_words_20)[:,1], tick_label=np.array(most_common_words_20)[:,0])
plt.title("20 Most Common Words in Julius Caezar")
plt.show()


"""Using Partitions for Parallelization"""
"""Calculate top 20 words in all of the files that you just read"""
# The way the information was read in (as just all the words in one batch) as opposed to
# seperate files in an RDD I assume this means top 20 words in totality of all the files as
# opposed to the top 20 files for each file seperately.
# For the other version it would make more sense to use the 'wholeTextFiles() method.

shakesrdd=sc.textFile("C:/Users/Lukas Buteliauskas/Desktop/Springboard Projects/18.3 MapReduce with Spark/sparklect/shakes/*.txt", minPartitions=4)

filtered_shakes_words=shakesrdd.flatMap(lambda x: x.split()).filter(lambda x: x.lower() not in stop_words)
most_common_shakes_words_20=filtered_shakes_words.map(lambda x: (x,1)).reduceByKey(lambda x,y: x+y).takeOrdered(20, key=lambda x: -x[1])
print("20 Most Common words in Shakespeare files:\n", most_common_shakes_words_20)

# I'm aware that more preprocessing steps could have been taken to take away punctuation and to lowercase words to get correct tallies.
# I'm happy to do those steps if necessary, however given that the purpose of this exercise is to get the hang of spark
# I've decided to keep the code as simple as possible.



