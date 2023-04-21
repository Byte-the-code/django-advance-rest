from django.contrib import admin

from admin_settings.models import Color, MeasureUnit, Category, SubCategory

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    fields = ['name']

@admin.register(MeasureUnit)
class MeasureUnitAdmin(admin.ModelAdmin):
    fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'category']