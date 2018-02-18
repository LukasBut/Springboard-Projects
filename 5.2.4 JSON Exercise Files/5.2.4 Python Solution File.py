# Importing necessary modules 
import pandas as pd
from pandas.io.json import json_normalize

#Reading in json file as a Dataframe from the exercise folder located on my desktop
projects_df=pd.read_json("C:/Users/Lukas Buteliauskas/Desktop/data_wrangling_json/data/world_bank_projects.json")

#Getting an overview of the structure of the DataFrame
print(projects_df.info(),"\n")

#Filtering the DataFrame to keep only the relevant columns for the task of finding the top 10 countries by number of projects
projects_df=projects_df[["mjtheme","project_name","mjtheme_namecode","theme_namecode","countryname"]]

#Count how many rows (projects) each other Country appears in, then sort descending and slice top 10
print("Top 10 Countries", "\n", projects_df["countryname"].value_counts().sort_values(ascending=False)[:10],"\n")

#Create a list of lists of values from the mjtheme_namecode column
list_of_lists=list(projects_df["mjtheme_namecode"].values)
#and generate a list of dictionaries of code:name pairs to use as input for json_normalize
list_of_dicts=[dict(key_value_pair) for json_list in list_of_lists for key_value_pair in json_list]

#Creating a Dataframe of theme names (name column) and their code (code column)
major_themes=json_normalize(list_of_dicts)

#Testing how many unique codes there actually are.
print("There are %d unique 'major themes codes'\n" % (len(major_themes["code"].unique())))

#Given the small number of unique codes we can consider them as a category.
major_themes["code"]=major_themes["code"].astype("category")

#Define a dictionary to be used in the function replace_emptry_entries.
unique_dict={code:name for code in major_themes["code"].unique() for name in major_themes.loc[major_themes["code"]==code,"name"].values if name!=""}

#The function that will aid us in filling in rows with code column entries, but no name column entries.
def replace_empty_entries(row):
    return unique_dict[row["code"]]

#Print output of the top 10 major project themes by count in descending order.
print("Top 10 Major Themes", "\n", major_themes["name"].value_counts().sort_values(ascending=False)[:10], "\n")

#Applying the function above to generate a column with no empty string values and convert to categorical variable to save space.
major_themes["name"]=major_themes.apply(replace_empty_entries,axis=1).astype("category")

#As required by point 3 in the exercises, here is the print output of the complete code:name DataFrame.
print(major_themes,"\n")


    
 




