# Springboard JSON Exercise Documentation

The problem was formatted as follows (sliderule_dsi_json_exercise.ipynb includes the full exercise formulation):
Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
1.Find the 10 countries with most projects
2.Find the top 10 major project themes (using column 'mjtheme_namecode')
In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

After importing the necessary modules I proceeded to read in the .json file as a local file. I didn't read it in as a URL as the URL to the Data source at
which the json could be found took me to a Wordpress login page. Given the assumption that access to the file via a URL was not a possibility I read
it in locally. I recognise that for the code to run on another machine the file path will need to be re-specified as appropriate and hence reading the 
json from a URL would have solved that issue.

On line 9 the .info() call on the dataframe was done to help me see the structure of the file. With the help of a chrome extension 'JSON Formatter' and 
the .info() call I saw that alot of the columns could be discarded for the purposes of the exercise, that there were numerous string entries ("")
and that there were 500 rows of input. Hence, the code on line 12. Granted, in retrospect, it could also have been possible to keep only a single column
with no empty string entries (the 'countryname' column) and the 'mjtheme_namecode' column which would be required for the further parts of the exercise.

The method chained call on line 14 extracted a sorted, sliced Pandas series of the top 10 countries by project count. I used .value_counts()
as opposed to .groupby("countryname")[*some_other_column_name*] due to its elegance and no need to aggregate by another column. I chained .sort_values()
at the end to avoid an unnecessary line of code.

Having looked at the documentation for json_normalize I saw that I needed to pass a dictionary of a list of dictionaries. Hence the next 2 lines of code.
The first extracts a numpy array from a Pandas series via the .values attribute which is then converted to a list list_of_lists. The second is a dictionary comprehension
that loops over the list of lists (entries in the mjtheme_namecode), and the inner for loop loops over the sets of code:name (key:value) pairs and 
casts them to a dictionary before appending to list_of_dicts. Then, finally the call to json_normalize() is made to create a DataFrame of only the 
code and name columns. This approach to producing a DataFrame for the mjtheme_namecode column seemed quite inelegant, but I couldn't find another way to
do it given the expected parameter type of json_normalize (dict, or list of dicts) and the requirement by the exercise formulation to use the method
("...and the techniques demonstrated above").

Given the small range of values of the code column (line 26) it made sense to consider it as a categorical variable for the purposes of saving space
and speeding up computations, hence the conversion to categorical via .astype("category") on line 29.

For the purposes of producing a Dataframe of the mjtheme_namecode column with no emptry string entried in the name column I created a dictionary
unique_dict which contained unique code:name pairs so that in my custom made function for any value in the 'code' column I could access a unique 
'name' column value from unique_dict and hence redefine the 'name' column and in doing so fulfill the 3rd requirement of the exercise.
The use of .apply() as opposed to using a for loop is once again based on a speed consideration.

Using the same reasoning as before, the 'name' column values are converted to categorical.

Line 42 prints the complete dataframe to highlight the successful transformation.

Line 45, in exactly the same fashion to the previous call to find the top 10 countries by count of project, finds the top 10 project themes and prints them.

The code omits certain dataframe prints and a few intermediate steps while trying to understand the structure of the json file and so on as it does not
contribute to the solution of the exercise.
Hopefully this provides enough justification for the programming choices made. I can't help but feel that there are possibly more elegant solutions
that don't require creation of separate dictionaries for example to achieve the same result so do feel free to share those suggestions. Thanks!




