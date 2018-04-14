import numpy as np
import pandas as pd
with open("C:/Users/Lukas Buteliauskas/Desktop/Springboard Projects/Capstone Project 1 - NBA Analytics/Player Data.csv", "r") as player_data:
    player_data_df=pd.read_csv(player_data)

player_data_df=player_data_df.replace("-1", np.nan)
# Deleting irrelevant columns.
player_data_df.drop(["Unnamed: 0"], axis="columns", inplace=True)

# Changing column variable types.
for column in ["Age", "G", "GS", "Year in League"]:
       player_data_df[column]=player_data_df[column].astype("int")
    
for column in ["Tm", "Country or State", "US or EU"]:
    player_data_df[column]=player_data_df[column].astype("category") 

# Labelling missing values
player_data_df=player_data_df.replace(-1, np.nan)

# Checking 'US or EU' column values
unique_places=player_data_df[player_data_df["US or EU"]=="Neither"]["Country or State"].unique()
"""print(player_data_df[player_data_df["US or EU"]=="Neither"]["Country or State"])"""
# 574/5122 rows have a 'Neither' US or EU column label. We need to do something.
"""for place in unique_places:
    print(place)"""
# We see that 32 countries/places are given a 'Neither' tag in the dataframe. 
# fyr macedonia and bosnia are in Europe, so we should correct their 'US or EU' column values.
player_data_df.loc[player_data_df["Country or State"]=="fyr macedonia","US or EU"]="EU"
player_data_df.loc[player_data_df["Country or State"]=="bosnia and herzegovina","US or EU"]="EU"
# Now let's deal with Canada.
"""print(player_data_df.loc[player_data_df["Country or State"]=="canada",["Country or State","US or EU"]])"""
# We see that 78 rows of data are from Canadian players. Considering the proximity
# of Canada to the US and the fact that the Toronto Raptors are also in the NBA,
# we might (for the purposes of this project) consider Canadian players fall under
# the US tag in terms of comparing players.
player_data_df.loc[player_data_df["Country or State"]=="canada","US or EU"]="US"
player_data_df.loc[player_data_df["Country or State"]=="u.s. virgin islands","US or EU"]="US"

"""print(player_data_df[player_data_df["US or EU"]=="Neither"]["Country or State"])"""
# We still have 461 rows that dont have a US or EU label, however since it would
# not make sense to assign those labels, we have to get rid of this data.
player_data_df=player_data_df[player_data_df["US or EU"]!="Neither"]
#Getting rid of NaN values in 'US or EU' column. Only 9 rows so no problem.
player_data_df=player_data_df.iloc[9:,:].reset_index()
player_data_df.drop(["index"], axis="columns", inplace=True)

print(player_data_df)
print(player_data_df.info())
print(player_data_df[player_data_df["2P"].isnull()]["2P"])

