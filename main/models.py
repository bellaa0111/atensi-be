from email.policy import default
from django.db import models
from main.utils.enums import JenisPertanyaan
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.
class Divisi(models.Model):
    name = models.CharField(max_length=100)
    akronim = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Jabatan(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TipePertanyaan(models.Model):
    tipe = models.CharField(max_length=50)

    def __str__(self):
        return self.tipe


class Kompetensi(models.Model):
    name = models.CharField(max_length=100)
    tipe_pertanyaan = models.ForeignKey(TipePertanyaan, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50)
    NPM = models.BigIntegerField(unique=True)
    divisi = models.ForeignKey(Divisi, on_delete=models.CASCADE)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
    tipe_pertanyaan = models.ManyToManyField(TipePertanyaan)

    def __str__(self):
        return self.name

class Pertanyaan(models.Model) :
    pertanyaan = models.TextField()
    jenis_pertanyaan = models.CharField(max_length=10, choices=JenisPertanyaan.choices, default=JenisPertanyaan.LIKERT)
    tipe_pertanyaan = models.ForeignKey(TipePertanyaan, on_delete=models.CASCADE)
    kompetensi_pertanyaan = ChainedForeignKey(Kompetensi, chained_field='tipe_pertanyaan', chained_model_field='tipe_pertanyaan', null = True)
    
    def __str__ (self) :
        return (f"{self.pertanyaan} ({self.tipe_pertanyaan})")


class Penilaian(models.Model):
    id_penilai = models.ForeignKey(
        User, verbose_name="Nama Penilai", related_name="penilai", on_delete=models.CASCADE)
    id_dinilai = models.ForeignKey(
        User, verbose_name="Nama Dinilai", related_name="dinilai", on_delete=models.CASCADE)
    value = models.JSONField(null=True, blank=True, verbose_name="Jawaban")
    done = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return str(self.id_penilai) + " menilai " + str(self.id_dinilai)

class OpenSheet(models.Model) :
    name = models.CharField(max_length = 200)

    def __str__(self) :
        return self.name
