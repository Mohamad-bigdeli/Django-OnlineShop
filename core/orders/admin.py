from django.contrib import admin
import openpyxl.workbook
from .models import Oreder, OrderItem
import openpyxl
from django.http import HttpResponse

# Actions

def export_to_exel(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=orders.xlsx"
    #------------------------
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orders"
    #------------------------
    columns = ['ID', 'First Name', 'Last Name', 'Phone', 'Address', 'Postal Code', 
               'Province', 'City', 'Paid', 'Created']
    ws.append(columns)
    #------------------------
    for order in queryset:
        created = order.created.replace(tzinfo=None) if order.created else ''
        ws.append([order.id, order.first_name, order.last_name, order.phone, order.address,
                    order.postal_code, order.province, order.city, order.paid, created])
    wb.save(response)
    return response

export_to_exel.short_description = "Export To Exel"

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    row_id_fields = ['product']

@admin.register(Oreder)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'first_name', 'last_name', 'phone', 'address', 'postal_code', 'province', 'city', 'paid', 'created']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_exel]