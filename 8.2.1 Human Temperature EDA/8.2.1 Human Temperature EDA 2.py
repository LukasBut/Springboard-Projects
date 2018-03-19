import pandas as pd

df = pd.read_csv('data/human_body_temperature.csv')

# Importing necessary modules
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set()

#Generating arrays for the ECDF (graphing original data)
ecdf_x=np.sort(df["temperature"])
ecdf_y=np.arange(1, len(ecdf_x)+1)/len(ecdf_x)

#Plotting the ECDF with an appropriate label and labelling the axes.
plt.plot(ecdf_x, ecdf_y, marker=".", linestyle="none", color="blue", label="Empirical CDF")
plt.xlabel("Temperature")
plt.ylabel("ECDF")

#Generating a sorted array of normally distributed values and the accompanying y axis values.
normal_samples=np.sort(np.random.normal(np.mean(df["temperature"]),np.std(df["temperature"]) , size=10000))
cdf_y=np.arange(1, len(normal_samples)+1)/len(normal_samples)

#Plotting the Theoretical CDF of the normally distributed data on top of the ECDF.
plt.plot(normal_samples, cdf_y, color="red", label="Theoretical CDF")
plt.legend(loc="upper left")

#Showing the Empirical and Theoretical CDFs on one graph.
plt.show()


#Calculating sample mean, standard deviation. Setting the proposed population mean.
sample_mean=np.mean(df["temperature"])
proposed_mean=98.6
sample_std=np.std(df["temperature"], ddof=1)

#Observed t value 
actual_t_value=(sample_mean - proposed_mean)/(sample_std / np.sqrt(len(df["temperature"])))

#Generating array to hold t values generated from bootstrap samples (bootstrap replicates)
t_values=np.empty(10000)

#Looping 10,000 times
for i in range(10000):
   # to generate bootstrap replicates and store them in the array
   simulated_sample=np.random.choice(df["temperature"], len(df["temperature"]))
   simulated_mean=np.mean(simulated_sample)
   simulated_std=np.std(simulated_sample, ddof=1)                                                                       
   t_values[i]=(simulated_mean - proposed_mean)/(simulated_std / np.sqrt(len(simulated_sample)))

#Calculating the p value   
p_value=np.sum(t_values>actual_t_value)/len(t_values)

print("Actual t value: %f, p value: %f\n" % (actual_t_value, p_value))
plt.hist(t_values, bins=50, normed=True, label="Simulated t values")
plt.xlabel("t value")
plt.ylabel("Probability")
plt.xticks([-x for x in range(1,11)])
plt.axvline(x=actual_t_value, color="red", label="Actual t value")
plt.legend(loc="upper left")
plt.show()


t_values_10_sample=np.empty(10000)

for i in range(10000):
   # to generate bootstrap replicates and store them in the array
   simulated_sample=np.random.choice(df["temperature"], 10)
   simulated_mean=np.mean(simulated_sample)
   simulated_std=np.std(simulated_sample)
   t_values_10_sample[i]=(proposed_mean - simulated_mean)/(simulated_std / np.sqrt(len(simulated_sample)))

p_value_10_sample=np.sum(t_values_10_sample>actual_t_value)/len(t_values_10_sample)

print("Actual t value: %f, p value (for sample of 10): %f\n" % (actual_t_value, p_value_10_sample))
plt.hist(t_values_10_sample, bins=50, normed=True, label="Simulated t values")
plt.xlabel("t value")
plt.ylabel("Count")
plt.axvline(x=actual_t_value, color="red", label="Actual t value")
plt.legend(loc="upper left")
plt.show()

sns.boxplot(x="gender", y="temperature", data=df, axis=1)
sns.swarmplot(x="gender", y="temperature", data=df, axis=1)
plt.plot()