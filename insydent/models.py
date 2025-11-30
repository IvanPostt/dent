from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name=("Название"))
    description = models.TextField(null=True, blank=True, verbose_name=("Описание"))

    class Meta:
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name=("Название"))
    description = models.TextField(null=True, blank=True, verbose_name=("Описание"))
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=("Цена"))
    quantity = models.PositiveIntegerField(default=0, verbose_name=("Количество"))
    image = models.ImageField(upload_to='products_images', blank=True, null=True, verbose_name=("Изображение"))
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name=("Категория"))

    class Meta:
        verbose_name = ("Продукт")
        verbose_name_plural = ("Продукты")

    def __str__(self):
        return f'{self.name} | {self.category.name}'