from django.contrib import admin

from products.models import Product, ExtraImage

class ExtraImageInline(admin.TabularInline):
    model = ExtraImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ExtraImageInline]

admin.site.register(Product, ProductAdmin)
