from django.contrib import admin

from products.models import Product, ExtraImage, Order

class ExtraImageInline(admin.TabularInline):
    model = ExtraImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ExtraImageInline]

admin.site.register(Product, ProductAdmin)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'creation_date', 'is_paid', 'remainder_sended')