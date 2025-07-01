from django.contrib import admin
from .models import transactions,Goal

##for the report export
from import_export import resources
from import_export.admin import ExportMixin


class tranImportExport(resources.ModelResource):
    class Meta:
        model=transactions
        fields=('title','date','amount','transaction_type')

class transactionAdmin(ExportMixin,admin.ModelAdmin):
    resource_classes=[tranImportExport]
    list_display=('title','date','amount','transaction_type')
    search_fields=('title',)

# Register your models here.
admin.site.register(transactions,transactionAdmin)
admin.site.register(Goal)


