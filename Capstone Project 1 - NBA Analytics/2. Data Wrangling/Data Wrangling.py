import numpy as np
import pandas as pd
with open("C:/Users/Lukas Buteliauskas/Desktop/Springboard Projects/Capstone Project 1 - NBA Analytics/Player Data.csv", "r") as player_data:
    player_data_df=pd.read_csv(player_data)

player_data_df=player_data_df.replace("-1", np.nan)
player_data_df.drop(["Unnamed: 0"], axis="columns", inplace=True)

# Changing column variable types.
for column in ["Age", "G", "GS"]:
       player_data_df[column]=player_data_df[column].astype("int")
    
for column in ["Tm", "Country or State", "US or EU", "Year in League", "G", "GS"]:
    player_data_df[column]=player_data_df[column].astype("category") 

# Labelling missing values
player_data_df=player_data_df.replace(-1, np.nan)

# Correcting 'US or EU' values.
player_data_df.loc[player_data_df["Country or State"]=="fyr macedonia","US or EU"]="EU"
player_data_df.loc[player_data_df["Country or State"]=="bosnia and herzegovina","US or EU"]="EU"
player_data_df.loc[player_data_df["Country or State"]=="canada","US or EU"]="US"
player_data_df.loc[player_data_df["Country or State"]=="u.s. virgin islands","US or EU"]="US"

# Getting rid of player data not from the US or EU.
player_data_df=player_data_df[player_data_df["US or EU"]!="Neither"]
# Getting rid of NaN values in 'US or EU' column.
player_data_df=player_data_df.iloc[9:,:].reset_index(drop=True)
# Getting rid of seasons where players didn't play.
player_data_df=player_data_df[player_data_df["2P"].notnull()].reset_index(drop=True)

player_data_df_og=player_data_df.copy(deep=True)

player_data_df.drop(["3P%", "FT%"], axis=1, inplace=True)
player_data_df=player_data_df[player_data_df["2P%"].notnull()].reset_index(drop=True)

player_data_df["2P%"]=player_data_df["2P%"]*100
player_data_df["eFG%"]=player_data_df["eFG%"]*100

print(player_data_df.info())

# Exporting dataframe
player_data_df.to_csv("Player Data Clean.csv")

