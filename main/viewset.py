from main.models import Pertanyaan, User, Penilaian, OpenSheet
from main.serializers import UploadSerializer, DataSerializerAllDinilai, DataSerializerListPertanyaan, DataSerializerUser, Penilaian, Data, DataSerializerPenilaian, PenilaianSerializer, PertanyaanSerializer, Pertanyaan as PertanyaanSerialize, UserSerializer
from main.sheets import  insert_data_kuantitatif
from main.sheets_kualitatif import insert_data_kualitatif
from main.csv_reader import *

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import JsonResponse

import pandas as pd

import io
import csv


class PenilaianViewSet(viewsets.ModelViewSet):
    queryset = Penilaian.objects.all()
    serializer_class = PenilaianSerializer
    def list(self, request) :
        queryset = Penilaian.objects.all()
        data = Data(queryset)
        serializer = DataSerializerPenilaian(data)
        return Response(serializer.data)

    def update(self, request, pk):
        try :
            message = ""
            status = True

            submitted_value = request.data['value']
            user_dinilai = Penilaian.objects.get(
                id_dinilai=pk, id_penilai=request.data['id_penilai'])

            # Update jawaban value
            user_dinilai.value = submitted_value
            user_dinilai.done = True
            user_dinilai.save()

            # Update Sheet
            user = User.objects.get(id = pk)
            sheet = OpenSheet.objects.all()
            if(len(sheet) == 0) :
                return JsonResponse({"message": "Please Add 'Oppen Sheet' for sheet name in Admin page"})
            kuantitatif_res = {}
            kualitatif_res = {}

            dinilai = Penilaian.objects.filter(id_dinilai = pk)
            for k in dinilai :
                penilai = User.objects.get(pk = k.id_penilai.id)
                if k.value != None :
                    for i in k.value :
                        if isinstance(i['jawaban'], int) :
                            if(kuantitatif_res.get(i['kompetensi']) != None) :
                                kuantitatif_res[i['kompetensi']]['jumlah'] = kuantitatif_res[i['kompetensi']]['jumlah'] + 1
                                kuantitatif_res[i['kompetensi']]['nilai'] =  (kuantitatif_res[i['kompetensi']]['nilai'] + i['jawaban'])
                            else :
                                kuantitatif_res[i["kompetensi"]] = {'jumlah' : 1, 'nilai' : i['jawaban']}
                        else :
                            if(kualitatif_res.get(i['id_pertanyaan']) != None) :
                                kualitatif_res[i["id_pertanyaan"]].append({'nama' : penilai.name, 'jawaban' : i['jawaban']})
                            else :
                                kualitatif_res[i["id_pertanyaan"]] = [{'nama' : penilai.name, 'jawaban' : i['jawaban']}]


            for i in kuantitatif_res :
                kuantitatif_res[i]['nilai'] /= kuantitatif_res[i]['jumlah']
                kuantitatif_res[i]['nilai'] = round(kuantitatif_res[i]['nilai'], 2)
            if len(kuantitatif_res.keys()) > 0 :
                insert_data_kuantitatif(kuantitatif_res, user, sheet[0])
            if len(kualitatif_res.keys()) > 0 :
                insert_data_kualitatif(kualitatif_res, user, sheet[0])
            return Response({"success": status,"message": message})
        except :
            message = "Please insert kompetensi, jumlah, and nilai on request body"
            status = False
            return Response({"success": status,"message": message})

    @action(detail=True)    
    def menilai(self, request, pk=None):
        queryset = Penilaian.objects.filter(id_penilai=pk)
        data = Data(queryset)
        serializer = DataSerializerAllDinilai(data)
        return Response(serializer.data)



class PertanyaanViewSet(viewsets.ModelViewSet):
    queryset = Pertanyaan.objects.all()
    serializer_class = PertanyaanSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.get(id=pk)
        tipe_pertanyaan = []
        temp = []

        tipe_pertanyaan_user = queryset.tipe_pertanyaan.all()

        #memilih pertanyaan berdasarkan tipe
        for i in tipe_pertanyaan_user:
            temp.append(i.id)

        #refactor response tipe pertanyaan
        for i in tipe_pertanyaan_user :
            tipe_pertanyaan.append(i.tipe)

        pertanyaan = Pertanyaan.objects.filter(
            tipe_pertanyaan__in=temp)
            
        s = PertanyaanSerialize(
            data=pertanyaan, tipe_pertanyaan=tipe_pertanyaan, name=queryset.name)
        data_set = Data(s, s.rows)
        dataSerializer = DataSerializerListPertanyaan(data_set)
        return Response(dataSerializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def user_detail(self, request):
        try:
            queryset = User.objects.get(NPM=request.data['NPM'])  
            data = Data(queryset)
            dataSerializer = DataSerializerUser(data)
            return JsonResponse(dataSerializer.data)
        except:
            return JsonResponse({"data": "Record Not Found"})

class FileUploadViewSet(viewsets.ViewSet) :
    serializer_class =  UploadSerializer

    def create(self, request) :
        file = request.data['file']
        content_type = file.content_type

        if content_type != 'text/csv' :
            response = "Please insert csv file"
            return Response(response)
        else :
            jenis = request.query_params.get('jenis')
            try :
                spamreader = pd.read_csv(file, sep=";")
                if(len(spamreader.columns) < 2) :
                    return Response(f"The file needs to be saved as CSV UTF-8 (Comma Delimited)")
                if jenis == "penilaian" :
                    response = insert_penilaian(spamreader)
                elif jenis == "kompetensi" :
                    response = insert_kompetensi(spamreader)
                elif jenis == "pertanyaan" :
                    response = insert_pertanyaan(spamreader)
                elif jenis == "user" :
                    response = insert_users(spamreader)
                else :
                    return Response(f"Format file does not match for input {jenis}")

                return Response(response)
            except Exception as e:
                return Response(str(e))

class IntegrateSheet(viewsets.ViewSet) :
    def list(self, request) :
        q = User.objects.all()
        sheet = OpenSheet.objects.all()
        if(len(sheet) == 0) :
            return JsonResponse({"message": "Please Add 'Oppen Sheet' for sheet name in Admin page"})
        for j in q :
            dinilai = Penilaian.objects.filter(id_dinilai = j.id)
            kuantitatif_res = {}
            kualitatif_res = {}
            for k in dinilai :
                penilai = User.objects.get(pk = k.id_penilai.id)
                if k.value != None :
                    for i in k.value :
                        if isinstance(i['jawaban'], int) :
                            if(kuantitatif_res.get(i['kompetensi']) != None) :
                                kuantitatif_res[i['kompetensi']]['jumlah'] = kuantitatif_res[i['kompetensi']]['jumlah'] + 1
                                kuantitatif_res[i['kompetensi']]['nilai'] =  (kuantitatif_res[i['kompetensi']]['nilai'] + i['jawaban'])
                            else :
                                kuantitatif_res[i["kompetensi"]] = {'jumlah' : 1, 'nilai' : i['jawaban']}
                        else :
                            if(kualitatif_res.get(i['id_pertanyaan']) != None) :
                                kualitatif_res[i["id_pertanyaan"]].append({'nama' : penilai.name, 'jawaban' : i['jawaban']})
                            else :
                                kualitatif_res[i["id_pertanyaan"]] = [{'nama' : penilai.name, 'jawaban' : i['jawaban']}]

            for i in kuantitatif_res :
                kuantitatif_res[i]['nilai'] /= kuantitatif_res[i]['jumlah']
                kuantitatif_res[i]['nilai'] = round(kuantitatif_res[i]['nilai'], 2)

            if len(kuantitatif_res.keys()) > 0 :
                insert_data_kuantitatif(kuantitatif_res, j, sheet[0])
            if len(kualitatif_res.keys()) > 0 :
                insert_data_kualitatif(kualitatif_res, j, sheet[0])
        return JsonResponse({"message": "Succes"})

