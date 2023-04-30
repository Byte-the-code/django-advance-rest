from django.db import models

from admin_settings.models import Color, MeasureUnit, Category, SubCategory

from users.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    SKU = models.CharField(max_length=20)
    price = models.FloatField()
    description = models.TextField()
    image_1 = models.ImageField(upload_to='product/images')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    is_distinguished = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_admin_banned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner.get_full_name()} - {self.name}'
    
    class Meta:
            verbose_name = 'Producto'
            verbose_name_plural = 'Productos'


class ExtraImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='product/extra-images/')

    def __str__(self):
        return f'{self.product.name} - {str(self.id)}'
    
    class Meta:
            verbose_name = 'Imagen extra de producto'
            verbose_name_plural = 'Imagenes extra de producto'
