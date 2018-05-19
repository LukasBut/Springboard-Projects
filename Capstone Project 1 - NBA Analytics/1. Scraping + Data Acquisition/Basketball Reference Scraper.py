""" This Python file is a web scraper for www.basketball-reference.com. It goes through the player index
URLs (for each letter from a-z, excluding 'x' as there is no 'x' webpage) and extracts the individual player
URLs providing that the player is a Center and started playing after 1980. The reason for this is that
the 3 point shot was introduced in 1980. I use 'website', 'link' and 'URL' interchangeably in this doc.
After that each player data is scraped and appended to a 'player data' dataframe which is then written
to a .csv file.
"""
import numpy as np
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import fnmatch 
import re
from us.states import STATES as us_states

# Creating and filling dictionary of soup objects (letter website links)
base_link="https://www.basketball-reference.com"
player_link="https://www.basketball-reference.com/players/"
soups={}

#Going through each letter link (using ASCII convention)
for i in range(26):
    if(i!=23): # 'x' webpage does not exist
        soups[chr(97+i)]=BeautifulSoup(urlopen(player_link + chr(97+i) + "/"))
        print("Added '%s' soup object" % (chr(97+i)) )

# List to hold player links. 
player_links=[]

# Add player links to player_links list.
for key, letter_soup in soups.items():
    # First row is a header row, all the rest are players. Create a players list.
    player_rows=letter_soup.table.find_all("tr")[1:]
    counter=0
    
    #Choose only centers that began playing after 1980
    for idx, player in enumerate(player_rows):
        if int(player.td.string) >= 1980 and fnmatch.fnmatch(player.find_all("td")[2].string, "*C*"):
            player_links.append(base_link+player.th.a["href"])
            counter+=1
            
"""Collection of individual player URLs is done, now we begin creating the 'player data' dataframe."""         
        
player_data_df= player_df=pd.read_html(str(BeautifulSoup(urlopen(player_links[0])).table))[0].iloc[:-1, 0:30]
dataframe_index=1

countries=np.array(["albania","andorra","armenia","austria","azerbaijan","belarus","belgium",
                    " bosnia and herzegovina","bulgaria","croatia","cyprus","czech republic",
                    "denmark","estonia","finland","france","georgia","germany","greece","hungary",
                    "iceland","ireland","italy","kazakhstan","kosovo","latvia","liechtenstein",
                    "lithuania","luxembourg","macedonia","malta","moldova","monaco","montenegro",
                    "netherlands","norway","poland","portugal","romania","russia","san marino",
                    "serbia","slovakia","slovenia","spain","sweden","switzerland","turkey",
                    "ukraine","united kingdom","vatican city"])
states=np.empty(shape=len(us_states), dtype=object)
for index, state in enumerate(us_states):
    states[index]=str(state).lower()

for player_link in player_links[1:]: # Creating and adding player dataframes together.
    try: # Catching IncompleteRead exceptions and trying the read again.
        player_soup=BeautifulSoup(urlopen(player_link))
    except:
        print("Exception raised for player %d" % (dataframe_index))
        player_soup=BeautifulSoup(urlopen(player_link))
    
    player_df=pd.read_html(str(player_soup.table))[0].iloc[:-1, 0:30]
    
    # Adding relevant relevant individual player information to dataframe before appending.
    player_df["Year in League"]=player_df.index.values+1
    player_df["Weight"]=float(player_soup.find("span", {"itemprop":"weight"}).string[:-2])/2.20462
    player_df["Height"]=(float(player_soup.find("span", {"itemprop":"height"}).string[0])*0.3048 +
              float(player_soup.find("span", {"itemprop":"height"}).string[2:])*0.0254)
    
    # Adding the draft placing of the player
    draft_link=player_soup.find("a", {"href":re.compile("/teams/.../draft.html")})
    if draft_link!=None:
        draft_string=list(draft_link.parent.stripped_strings)[2]
        player_df["Draft Placing"]=draft_string[draft_string.find("pick, ")+6:draft_string.find(" overall")-2]
    else:
        player_df["Draft Placing"]=-1
        
    country_or_state=list(player_soup.find("span", {"itemprop":"birthPlace"}).stripped_strings)[1].lower()
    player_df["Country or State"]=country_or_state
    US_or_EU="Neither"
    if country_or_state in countries:
        US_or_EU="EU"
    if country_or_state in states:
        US_or_EU="US"
    player_df["US or EU"]=US_or_EU

    player_data_df=player_data_df.append(player_df)
    print("%d/%d dataframes appended" % (dataframe_index, len(player_links)-1))
    dataframe_index+=1

# Dropping some irrelevant columns.
player_data_df.drop(["Lg","Pos"], axis="columns", inplace=True)

# Writing the 'player data' dataframe to a .csv file.
player_data_df.to_csv("Player data.csv")

