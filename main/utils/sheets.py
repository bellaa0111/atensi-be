import pygsheets
import pandas as pd

def insert_data() : 
    #authorization
    gc = pygsheets.authorize(service_file='C:/Users/tantr/Downloads/rising-guide-352716-e76fbf2b5203.json')

    # Create empty dataframe
    df = pd.DataFrame()

    # Create a column

    df['name'] = ['John', 'Steve', 'Sarah']
    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('Test Sheet')

    #select the first sheet 
    sh.add_worksheet('test2')
    wks = sh[1]

    #update the first sheet with df, starting at cell B2. 
    wks.set_dataframe(df,(1,1))