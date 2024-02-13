import gspread
import pandas as pd
import os

from main.models import Pertanyaan

def get_dict_pertanyaan() :
    list_pertanyaan_object = Pertanyaan.objects.all()
    list_pertanyaan = {}

    for i in list_pertanyaan_object :
        list_pertanyaan[i.id] = i.pertanyaan
    
    return list_pertanyaan

def insert_data_kualitatif(x, dinilai, sheet) : 
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
        wks = sheet.worksheet(f"{dinilai.divisi.name} (Kualitatif)")
    except :
        sheet.add_worksheet(f"{dinilai.divisi.name} (Kualitatif)", rows=100, cols=26)
        wks = sheet.worksheet(f"{dinilai.divisi.name} (Kualitatif)")


    #create dataframe based on spreadsheets
    df = pd.DataFrame(wks.get_all_records())
    
    #mapping pertanyaan
    list_pertanyaan = get_dict_pertanyaan()

    if(df.empty) :
        kompetensi = {'Pertanyaan' : []}
        df = pd.DataFrame(kompetensi)

    if(dinilai.name not in df.columns) :
        df[dinilai.name] = ""
    for i in x :
        pertanyaan = list_pertanyaan[i]
        if(pertanyaan not in df.get("Pertanyaan").values) :
            df.loc[len(df)] = pertanyaan
            df.iloc[-1, 1:] = ""
        for j in x[i] :
            pertanyaan_index = df.index[df["Pertanyaan"] == pertanyaan][0]
            if(len(df.at[pertanyaan_index, dinilai.name]) == 0) :
                temp = f"{j['nama']}: {j['jawaban']}"
            else :
                temp = df.at[pertanyaan_index, dinilai.name] + f"\n\n{j['nama']}: {j['jawaban']}"
        df.at[pertanyaan_index, dinilai.name] = temp
    wks.update([df.columns.values.tolist()] + df.values.tolist())