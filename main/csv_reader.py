from main.models import User, Penilaian, TipePertanyaan, Kompetensi, Pertanyaan, Divisi, Jabatan
from django.db import transaction

@transaction.atomic
def insert_penilaian(spamreader) :
    dict_npm = {}
    list_npm = User.objects.all()

    for i in list_npm :
        dict_npm[i.NPM] = i

    for _, row in spamreader.iterrows():
        if row['id_penilai'] not in dict_npm.keys() :
            response = f"id_penilai {row['id_penilai']} does not exist"
            raise Exception(response)

        elif row['id_dinilai'] not in dict_npm.keys() :
            response = f"id_dinilai {row['id_dinilai']} does not exist"
            raise Exception(response)

        penilai = Penilaian(id_penilai = dict_npm[row['id_penilai']],
                            id_dinilai = dict_npm[row['id_dinilai']],
                            value = None,
                            done = False)
        penilai.save()

    response = "Success inserting data"
    return response

@transaction.atomic
def insert_kompetensi(spamreader) :
    dict_tipe_pertanyaan = {}
    list_tipe_pertanyaan = TipePertanyaan.objects.all()
    
    for i in list_tipe_pertanyaan :
        dict_tipe_pertanyaan[i.tipe] = i
    
    for _, row in spamreader.iterrows():
        if row['tipe_pertanyaan'] not in dict_tipe_pertanyaan.keys() :
            response = f"tipe_pertanyaan {row['tipe_pertanyaan']} does not exist"
            raise Exception(response)
        kompetensi = Kompetensi(name = row['name'],
                            tipe_pertanyaan = dict_tipe_pertanyaan[row['tipe_pertanyaan']])
        kompetensi.save()

    response = "Success inserting data"
    return response

@transaction.atomic
def insert_pertanyaan(spamreader) :
    dict_tipe_pertanyaan = {}
    dict_kompetensi_pertanyaan = {}

    list_tipe_pertanyaan = TipePertanyaan.objects.all()
    list_kompetensi_pertanyaan = Kompetensi.objects.all()


    for i in list_tipe_pertanyaan :
        dict_tipe_pertanyaan[i.tipe] = i

    for i in list_kompetensi_pertanyaan :
        dict_kompetensi_pertanyaan[i.name] = i
    
    for _, row in spamreader.iterrows():
        if row['tipe_pertanyaan'] not in dict_tipe_pertanyaan.keys() :
            response = f"tipe_pertanyaan {row['tipe_pertanyaan']} does not exist"
            raise Exception(response)

        if row['kompetensi_pertanyaan'] not in dict_kompetensi_pertanyaan.keys() :
            response = f"kompetensi_pertanyaan {row['kompetensi_pertanyaan']} does not exist"
            raise Exception(response)

        kompetensi_pertanyaan = dict_kompetensi_pertanyaan[row['kompetensi_pertanyaan']]
        tipe_pertanyaan = dict_tipe_pertanyaan[row['tipe_pertanyaan']]

        if kompetensi_pertanyaan.tipe_pertanyaan != tipe_pertanyaan :
            response = f"kompetensi_pertanyaan {kompetensi_pertanyaan} not available for tipe_pertanyaan {tipe_pertanyaan}"
            raise Exception(response)

        pertanyaan = Pertanyaan(pertanyaan = row['pertanyaan'],
                            jenis_pertanyaan =row['jenis_pertanyaan'],
                            tipe_pertanyaan = dict_tipe_pertanyaan[row['tipe_pertanyaan']],
                            kompetensi_pertanyaan = dict_kompetensi_pertanyaan[row['kompetensi_pertanyaan']]
                            )
        pertanyaan.save()
    response = "Success inserting data"
    return response

@transaction.atomic
def insert_users(spamreader) :
    dict_divisi = {}
    dict_jabatan = {}
    dict_tipe_pertanyaan = {}

    list_divisi = Divisi.objects.all()
    list_jabatan = Jabatan.objects.all()
    list_tipe_pertanyaan = TipePertanyaan.objects.all()

    for i in list_divisi :
        dict_divisi[i.name] = i
    
    for i in list_jabatan :
        dict_jabatan[i.name] = i
    
    for i in list_tipe_pertanyaan :
        dict_tipe_pertanyaan[i.tipe] = i

    for _, row in spamreader.iterrows():
        list_tipe_pertanyaan_user = row['tipe_pertanyaan'].split(',')
        if row['divisi'] not in dict_divisi.keys() :
            raise Exception(f"divisi {row['divisi']} does not exist")
        
        elif row['jabatan'] not in dict_jabatan.keys() :
            raise Exception(f"jabatan {row['jabatan']} does not exist")

        user = User(name = row['name'],
                    NPM = int(row['npm']),
                    divisi = dict_divisi[row['divisi']],
                    jabatan = dict_jabatan[row['jabatan']])
        user.save()

        for i in list_tipe_pertanyaan_user :
            if i not in dict_tipe_pertanyaan.keys() :
                raise Exception(f"tipe_pertanyaan {row['tipe_pertanyaan']} does not exist")
            user.tipe_pertanyaan.add(dict_tipe_pertanyaan[i])

    response = "Success inserting data"
    return response