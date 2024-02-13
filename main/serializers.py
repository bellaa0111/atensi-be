from dataclasses import field
from main.models import Pertanyaan as P, Penilaian, User, Divisi, TipePertanyaan
from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField


class TipePertanyaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipePertanyaan
        fields = ['tipe']


class PenilaianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penilaian
        fields = ['id_penilai', 'id_dinilai', 'value']


class UserIntermediate(serializers.ModelSerializer):
    jabatan = serializers.StringRelatedField()
    divisi = serializers.StringRelatedField()

    akronim = serializers.SerializerMethodField('get_akronim')
    class Meta:
        model = User
        fields = ['id', 'name', 'jabatan', 'divisi', 'akronim']
    
    def get_akronim(self, obj) :
        return obj.divisi.akronim


class DivisiSerilizers (serializers.ModelSerializer):
    class Meta:
        model = Divisi
        fields = ['name', 'akronim']


class UserSerializer(serializers.ModelSerializer):
    divisi = serializers.StringRelatedField()
    jabatan = serializers.StringRelatedField()

    tipe_pertanyaan = serializers.SerializerMethodField('get_tipe_pertanyaan')
    akronim = serializers.SerializerMethodField('get_akronim')
    class Meta:
        model = User
        fields = ['id', 'name', 'NPM', 'divisi',
                  'akronim', 'jabatan', 'tipe_pertanyaan']

    def get_akronim(self, obj):
        return obj.divisi.akronim

    def get_tipe_pertanyaan(self, obj):
        list_tipe_pertanyaan = []
        tipe_pertanyaan = obj.tipe_pertanyaan.all()
        for i in tipe_pertanyaan:
            list_tipe_pertanyaan.append(i.tipe)
        return list_tipe_pertanyaan


class ListPenilaianSerializer(serializers.ModelSerializer):
    user_dinilai = UserIntermediate(source="id_dinilai", read_only=True)

    class Meta:
        model = Penilaian
        fields = ['done', 'user_dinilai']


class PertanyaanSerializer(serializers.ModelSerializer):
    kompetensi_pertanyaan = serializers.SerializerMethodField('get_id_kompetensi')

    class Meta:
        model = P
        fields = ['id', 'pertanyaan',
                  'jenis_pertanyaan', 'kompetensi_pertanyaan']

    def get_id_kompetensi(self, obj):
        return obj.kompetensi_pertanyaan.id


class Data:
    def __init__(self, data_set, pertanyaans=None):
        self.data = data_set
        self.pertanyaan = pertanyaans


class Pertanyaan:
    def __init__(self, name, tipe_pertanyaan, data):
        self.name = name
        self.tipe_pertanyaan = tipe_pertanyaan
        self.rows = data


class PertanyaanListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    tipe_pertanyaan = serializers.ListField(
        child=serializers.CharField(max_length=200)
    )
    rows = PertanyaanSerializer(many=True)


class DataSerializerListPertanyaan(serializers.Serializer):
    data = PertanyaanListSerializer()


class DataSerializerPenilaian(serializers.Serializer):
    data = PenilaianSerializer(many=True)


class DataSerializerAllDinilai(serializers.Serializer):
    data = ListPenilaianSerializer(many=True)


class DataSerializerUser(serializers.Serializer):
    data = UserSerializer()

class UploadSerializer(Serializer):
    file = FileField()
    class Meta:
        fields = ['file']
