from django.db import models

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    qty = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Supply(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.product.name} от {self.supplier.name}"
