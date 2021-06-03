import pandas as pd
import matplotlib.pyplot as plt

#Dataset downloaded from https://github.com/LearnDataSci/articles/blob/master/Python%20Pandas%20Tutorial%20A%20Complete%20Introduction%20for%20Beginners/IMDB-Movie-Data.csv
#Defining the CSV and index column name
FILE_PATH = 'IMDB-Movie-Data.csv'
INDEX_COLUMN_NAME = 'Title'

def main():
    '''
     Execution starts here.
    '''
    print_intro()
    choice = user_input()
    movies_df = load_imdb_data(FILE_PATH,INDEX_COLUMN_NAME) #Load data
    movies_df = pre_process_df(movies_df) # Pre process the data as we need to define new columns and apply functions
    movies_df = impute_df(movies_df) #Impute data to avoid nulls
    #result of movies_df.isnull().sum() should be all 0s

    if(choice == 'a'):
        analyse_data(movies_df)  #Analyse module for the loaded dataset
    else:
        recommend_movie(movies_df) #Movie recommender based on the user input





def print_intro():
   
    print('*************************************************************************************')
    print('This project explores a 1000 movies dataset from ImDB between the years of 2006-2016')
    print('*************************************************************************************')
    print('Choose option a or b below to get started:')
    print('a) Analyse DataSet')
    print('b) Recommend movies based on Genre')

def user_input():
    '''
     Take user input to either analyse or recommend movie.
    '''
    choice = input('Enter your choice(a or b):')
    while(choice != 'a' and choice != 'b'):  #Invalid input handler
        print('Wrong choice entered.Please retry.')
        choice = input('Enter your choice(a or b):')
    return choice

def load_imdb_data(file,index_column):
    '''
     Load the dataset.
    '''
    df = pd.read_csv(file,index_col=index_column)
    return df


def pre_process_df(df):
    '''
    Function to pre-process data for further analysis 
    like renaming/adding columns,etc.
    '''
    df.rename(columns={'Runtime (Minutes)':'Runtime_In_Mins',
    'Revenue (Millions)':'Revenue_In_Millions'
    },inplace=True)
    df.columns = [col.lower() for col in df]
    df['actors_lower_case'] = df['actors'].str.lower() # Store lower case \n
    df['genres_lower_case'] = df['genre'].str.lower()  #values for comparision
    df['movie_time'] = df["runtime_in_mins"].apply(runtime_function)
    return df

def impute_df(df):
    '''
    Impute dataset to avoid null values in revenue and metascore 
    by using the mean of those columns as a default.
    '''
    #Imputing the revenue and metascore columns in place with the mean value
    revenue = df['revenue_in_millions']
    #Calculate mean in the series
    revenue_mean = revenue.mean()
    df['revenue_in_millions'].fillna(revenue_mean, inplace=True)
    meta_score = df['metascore']
    meta_score_mean = meta_score.mean()
    df['metascore'].fillna(meta_score_mean, inplace=True)
    return df


def analyse_data(df):
    '''
     Function to analyse dataset.
    '''
    print_analyse_intro()
    analysis_input(df)



def analysis_input(df):
    '''
    User input processing for dataset analysis
    '''

    choice_list = ['a','b','c','d','e']
    analysis_choice = input('Enter your data analysis choice(a,b,c,d,e):')   
    while(choice_list.count(analysis_choice) == 0):
        print('Wrong choice entered.Please retry.')
        analysis_choice = input('Enter your data analysis choice(a,b,c or d):')
    #Define a dictionary of functions to execute
    choice_dict = {'a':'five_highest_revenue(df)',
                   'b':'top_revenue_by_director(df)',
                   'c':'top_rated_by_act(df)',
                   'd':'plot_scat_graph(df)',
                   'e':'quit()',

    }
    eval(choice_dict[analysis_choice]) #Evaluate chosen input as a function


def five_highest_revenue(df):
    '''
    Find the top 5 highest revenue generating titles.
    '''
    print(df.sort_values(['revenue_in_millions'],ascending=[False])[['revenue_in_millions','runtime_in_mins']].head(5))
    print_analyse_intro()
    analysis_input(df)

def top_revenue_by_director(df):

    '''
     Take the user input to find out the top 3 revenue 
     generating titles for a given director.
    '''
    director = input('Please enter a Director\'s name:')
    director_df = df[df['director'] == director] #Query by the given director
    if(len(director_df) > 0):
        print(director_df.sort_values(['revenue_in_millions'],ascending=[False])['revenue_in_millions'].head(3)) #Sort and show top 3 titles
    else:
         retry = input('No movies exist in the dataset for \033[1;31;40m' + director + '\033[0;37;40m.Press \'r\' to re-enter.')
         while(retry == 'r'):
            retry = None
            top_revenue_by_director(df) #Recurse if retry is needed
    print_analyse_intro() #Let user continue
    analysis_input(df)

def top_rated_by_act(df):
    '''
     Take the user input for finding out the 
     top 3 rated movies for a given actor/actress.
    '''
    act = input('Please enter an Actor\'s or an Actress\'s name:')
    act_df = df[df['actors_lower_case'].str.contains(act.lower())] #Compare the user the input to filter actor/actress titles
    if(len(act_df) > 0):
        #pd.set_option('max_columns', None)
        pd.set_option('display.max_colwidth', None) #Print on a wider format
        print(act_df.sort_values(['rating'],ascending=[False])[['rating','actors']].head(3)) #Sort and display results
    else:
         retry = input('No movies exist in the dataset for \033[1;31;40m' + act + '\033[0;37;40m.Press \'r\' to re-enter.')
         while(retry == 'r'):
            retry = None
            top_rated_by_act(df) #Recurse if retry is needed
    print_analyse_intro() #Let user continue
    analysis_input(df)

def plot_scat_graph(df):
    '''
     Plot a scatter graph with matplotlib. 
    '''
    df.plot(kind='scatter', x='movie_time', y='revenue_in_millions', title='Revenue (in Millions) vs Runtime')
    plt.show()
    print_analyse_intro()
    analysis_input(df)

def runtime_function(x):
    '''
    Categorise the movie runtime with custom values.
    '''
    if x <= 90:
        return "Lesser than 2 hours"
    if(x >= 90 and x <= 120):
        return "Almost 2 hours"
    else:
        return "Greater than 2 hours"

def print_analyse_intro():

    print('******************************************************************************************************')
    print('We can analyse this dataset using a python package called pandas and plot the graphs using matplotlib.')
    print('******************************************************************************************************')
    print('Choose any option below to get started:')
    print('a) Find the top 5 highest revenue generating movies:')
    print('b) Enter a Director\'s name to show the top 3 revenue generating movies by him/her')
    print('c) Enter an Actor\'s/Actress\'s name to show his/her 3 highest rated movies')
    print('d) Plot a scatter graph to see the relationship between the runtime of a movie to it\'s revenue')
    print('e) Quit')





def recommend_movie(df):
    '''
     Movie recommender function.
    '''
    genre_options = extract_genres(df) #pull out all the genres from the dataset
    print_reco_intro(genre_options) 
    generate_recommendation(df,genre_options)
    
def extract_genres(df):
    '''
    Since Genres is a multi value column,we need to be able to 
    process it and pull out only the unique values.
    '''
    genre_unique_list_multi = list(df['genre'].unique())
    unique_string=''  #Initialise the string
    for item in genre_unique_list_multi:
        unique_string = unique_string + ',' + item.lower()
    unique_list_genres = unique_string.split(',')
    return list(set(unique_list_genres)) #Convert the list to set to remove duplicates and then return the unique valued list

def print_reco_intro(genre_options):
    '''
    Print the genre options to the user to choose from.
    '''
    print('**************************************')
    print('Choose a Genre to recommend popular titles')
    print('**************************************')
    print('Options are as follows:')
    print(genre_options[1:len(genre_options)]) #exclude the first value due to empty string and print rest of the items

def generate_recommendation(df,genre_options):
    '''
    Take user input for the genre and provide movie recommendation.
    '''
    user_genre = input('Choose your genre:')    
    while(user_genre.lower() not in genre_options):
        print('Invalid Input!!!Please Retry...')
        user_genre = input('Choose your genre:')    
    genre_df = df[df['genres_lower_case'].str.contains(user_genre.lower())] #Compare with lower case genre
    if(len(genre_df) > 0):
        #pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', None)  #Print results without width issues

        print('************************Popular and recommended titles for ' + user_genre + '***************************')
        print(genre_df.sort_values(['metascore'],ascending=[False])[['metascore','genre','description']].head(5)) #Print top 5 popular movie titles as a 
                                                                                                                  #recommendation based on genre

def quit():
    '''
    Quit application.
    '''
    exit()

if __name__ == '__main__':
    main()

