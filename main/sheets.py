import pandas as pd
import os
import gspread



from main.models import Kompetensi

def get_dict_kompetensi() :
    list_kompetensi_object = Kompetensi.objects.all()
    list_kompetensi = {}
    for i in list_kompetensi_object :
        list_kompetensi[i.id] = i.name
    return list_kompetensi

def insert_data_kuantitatif(x, dinilai, sheet) : 
    #authorization
    sheet_authorization = gspread.service_account(filename=os.getcwd()+'/bem_psiko_be/evaluation-program-353906-df7e66980a6f.json' )
    
    #open the google spreadsheet
    try :
        sheet = sheet_authorization.open(sheet.name)
    except :
        sheet_authorization.create(sheet.name)
        sheet = sheet_authorization.open(sheet.name)
        sheet.share('litbang.bempsikoui2022@gmail.com', role = 'writer', perm_type='user')
    try:   
        wks = sheet.worksheet(dinilai.divisi.name)
    except :
        sheet.add_worksheet(dinilai.divisi.name, rows=100, cols=26)
        wks = sheet.worksheet(dinilai.divisi.name)

    #create dataframe based on spreadsheets
    df = pd.DataFrame(wks.get_all_records())
    
    #mapping kompetensi
    list_kompetensi = get_dict_kompetensi()

    if(df.empty) :
        kompetensi = {'Kompetensi' : []}
        kompetensi['Kompetensi'].append("Final Score")
        df = pd.DataFrame(kompetensi)
    
    if(dinilai.name not in df.columns) :
        df[dinilai.name] = ""

    for i in x :
        kompetensi_name = list_kompetensi[i]
        if(kompetensi_name not in df.get("Kompetensi").values) :
            df.loc[len(df)]= df.loc[len(df) - 1]
            df.loc[len(df) - 2] = kompetensi_name
            df.iloc[-2, 1:] = ""
        kompetensi_index = df.index[df["Kompetensi"] == kompetensi_name][0]
        df.at[kompetensi_index, dinilai.name] = x[i]["nilai"]

    total_score = 0
    for i in df[dinilai.name][:-1] :
        if(isinstance(i, float) or isinstance(i, int)) :
            total_score += i
    final_score = round(((total_score/len(x.keys())) / 6 * 100),2)
    kompetensi_index = df.index[df["Kompetensi"] == "Final Score"][0]
    df.at[kompetensi_index, dinilai.name] = final_score

    wks.update([df.columns.values.tolist()] + df.values.tolist())