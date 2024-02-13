from django.contrib import admin
import pygsheets
from main.models import *
import os
# Register your models here.
class OpenSheetAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        divisi = OpenSheet.objects.count()
        if (divisi < 1) :
            return True
        return False

class UserAdmin(admin.ModelAdmin) :
    def has_change_permission(self, request, obj=None):
        return False
    
    def delete_model(self, request, obj):
        sheet = OpenSheet.objects.all()
        sheet_authorization = pygsheets.authorize(service_file=os.getcwd()+'/bem_psiko_be/evaluation-program-353906-df7e66980a6f.json')
        try :
            open_sheet = sheet_authorization.open(sheet[0].name)
            deleted_worksheet = open_sheet.worksheet_by_title(obj.name)
            open_sheet.del_worksheet(deleted_worksheet)
        except :
            pass
        obj.delete()
    
    def delete_queryset(self, request, queryset) :
        sheet = OpenSheet.objects.all()
        sheet_authorization = pygsheets.authorize(service_file=os.getcwd()+'/bem_psiko_be/evaluation-program-353906-df7e66980a6f.json')
        try :
            open_sheet = sheet_authorization.open(sheet[0].name)
            for i in queryset :
                deleted_worksheet = open_sheet.worksheet_by_title(i.name)
                open_sheet.del_worksheet(deleted_worksheet)
        except :
            pass
        queryset.delete()

class PertanyaanAdmin(admin.ModelAdmin) :
    def has_change_permission(self, request, obj=None):
        return False

class PenilaianAdmin(admin.ModelAdmin) :
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(User, UserAdmin)
admin.site.register(Pertanyaan, PertanyaanAdmin)
admin.site.register(Penilaian, PenilaianAdmin)
admin.site.register(TipePertanyaan)
admin.site.register(Divisi)
admin.site.register(Jabatan)
admin.site.register(Kompetensi)
admin.site.register(OpenSheet, OpenSheetAdmin)
